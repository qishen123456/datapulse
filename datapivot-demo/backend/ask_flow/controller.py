from __future__ import annotations

import os
import time
from copy import deepcopy
from typing import Any, Dict, Iterable, Optional

from config_manager import read_json
from datapulse_basic.service import basic_ask_service
from datapulse_advanced import advanced_ask_service
from ask_runtime import create_run, bind_run, AskCancelled, scope_key
from ask_workflow import catalog, business_event, result_outcome


from .contracts import AskRequest, ConfirmRequest, FlowDecision


DEFAULT_ASK_FLOW_CONFIG: Dict[str, Any] = {
    "defaultFlow": "basic",
    "advancedEnabled": False,
    "advancedRoles": ["super_admin"],
    "datasetPolicies": {},
    "rolePolicies": {},
    "fallbackToBasicOnError": False,
    "attachMetadata": True,
    "maxParallel": 3,
    "maxRetries": 2,
    "queryTimeoutSeconds": 30,
    "maxResultRows": 10000,
}
ADVANCED_ASK_FLOW_FEATURE_KEY = "advanced_ask_flow"


class AskFlowController:
    """Selects the ask engine while keeping the old basic flow untouched."""

    def __init__(self, basic_service=None, advanced_service=None):
        self.basic_service = basic_service or basic_ask_service
        self.advanced_service = advanced_service or advanced_ask_service

    def load_config(self) -> Dict[str, Any]:
        config = deepcopy(DEFAULT_ASK_FLOW_CONFIG)
        stored = read_json("ask_flow.json")
        if isinstance(stored, dict):
            for key, value in stored.items():
                if key in ("datasetPolicies", "rolePolicies") and isinstance(value, dict):
                    config[key].update(value)
                elif key in config:
                    config[key] = value

        env_default = (os.getenv("DATAPULSE_DEFAULT_FLOW") or "").strip().lower()
        if env_default in ("basic", "advanced"):
            config["defaultFlow"] = env_default

        env_advanced = (os.getenv("DATAPULSE_ADVANCED_FLOW_ENABLED") or "").strip().lower()
        if env_advanced in ("1", "true", "yes", "on"):
            config["advancedEnabled"] = True
        elif env_advanced in ("0", "false", "no", "off"):
            config["advancedEnabled"] = False
        for key, default, low, high in (("maxParallel",3,1,4),("maxRetries",2,0,2),("queryTimeoutSeconds",30,3,120),("maxResultRows",10000,100,20000)):
            try:
                config[key] = min(high,max(low,int(config.get(key,default))))
            except (ValueError,TypeError):
                config[key] = default
        config["fallbackToBasicOnError"] = False
        return config

    def active_service(self):
        return self.basic_service

    def route_with_agent1(self, *args, **kwargs) -> Dict[str, Any]:
        return self.basic_service.route_with_agent1(*args, **kwargs)

    def _role_allowed(self, user: Optional[Dict[str, Any]], config: Dict[str, Any]) -> bool:
        try:
            from feature_flags import feature_available
            if not feature_available(ADVANCED_ASK_FLOW_FEATURE_KEY, user or {}):
                return False
        except Exception:
            return False

        roles = config.get("advancedRoles") or []
        if not roles:
            return True
        allowed_roles = {str(item).strip() for item in roles if str(item).strip()}
        user_roles = set()
        role = str((user or {}).get("role") or "").strip()
        if role:
            user_roles.add(role)
        role_ids = (user or {}).get("role_ids")
        if isinstance(role_ids, list):
            user_roles.update(str(item).strip() for item in role_ids if str(item).strip())
        return bool(allowed_roles.intersection(user_roles))

    @staticmethod
    def _first_dataset_id(dataset_ids: Optional[Iterable[Any]]) -> str:
        for item in dataset_ids or []:
            try:
                return str(int(item))
            except Exception:
                continue
        return ""

    def decide(self, *, user: Optional[Dict[str, Any]], requested_flow: str = "", dataset_ids=None) -> FlowDecision:
        config = self.load_config()
        requested = str(requested_flow or "").strip().lower()
        dataset_policy = ""
        dataset_id = self._first_dataset_id(dataset_ids)
        policies = config.get("datasetPolicies") if isinstance(config.get("datasetPolicies"), dict) else {}
        if dataset_id:
            dataset_policy = str(policies.get(dataset_id) or "").strip().lower()

        # An explicit role assignment is authoritative, including against old clients.
        role_policies = config.get('rolePolicies') if isinstance(config.get('rolePolicies'),dict) else {}
        role_policy = role_policies.get(str((user or {}).get('role') or ''))
        candidate = role_policy if role_policy in ('basic','advanced') else requested if requested in ('basic','advanced') else ''
        if not candidate and dataset_policy in ("basic", "advanced"):
            candidate = dataset_policy
        if not candidate:
            candidate = str(config.get("defaultFlow") or "basic").strip().lower()
        if candidate not in ("basic", "advanced"):
            candidate = "basic"

        if candidate != "advanced":
            return FlowDecision("basic", "basic_selected", requested, config)
        if not bool(config.get("advancedEnabled")):
            return FlowDecision("basic", "advanced_disabled", requested, config)
        if not self._role_allowed(user, config):
            return FlowDecision("basic", "advanced_role_denied", requested, config)
        return FlowDecision("advanced", "advanced_selected", requested, config)

    def _service_for(self, decision: FlowDecision):
        if decision.flow == "advanced":
            return self.advanced_service
        return self.basic_service

    @staticmethod
    def _attach_metadata(result: Dict[str, Any], decision: FlowDecision, started: float) -> Dict[str, Any]:
        if not isinstance(result, dict):
            return result
        if decision.config.get("attachMetadata") is False:
            result.pop("ask_flow", None)
            diagnostics = result.get("diagnostics")
            if isinstance(diagnostics, dict):
                diagnostics.pop("ask_flow", None)
            return result
        metadata = {
            "flow": decision.flow,
            "reason": decision.reason,
            "requested_flow": decision.requested_flow,
            "controller": "AskFlowController",
            "duration_seconds": round(time.time() - started, 3),
        }
        result.setdefault("ask_flow", metadata)
        diagnostics = result.get("diagnostics")
        if isinstance(diagnostics, dict):
            diagnostics.setdefault("ask_flow", metadata)
        return result

    def _execute(self, request, *, confirmation=False):
        started = time.time()
        research_confirmation = confirmation and request.session_id.startswith("research-")
        requested = "advanced" if research_confirmation else request.requested_flow
        decision = self.decide(user=request.current_user, requested_flow=requested,
                               dataset_ids=request.selected_dataset_ids if confirmation else request.preferred_dataset_ids)
        # Explicit advanced requests never silently execute the ordinary path.
        if requested == "advanced" and decision.flow != "advanced":
            return {"error": "当前账号或控制台配置未开放高阶研究，请联系管理员核对问数授权。", "error_code":decision.reason,
                    "ask_flow":decision.to_dict()}
        service = self._service_for(decision)
        run = create_run(request.current_user or {}, request.allowed_dataset_ids, decision.flow, decision.config, request.execution_id)
        live = request.live_callback
        def emit(payload):
            event = business_event(payload, run)
            if decision.flow == 'advanced' and (payload.get('event') or {}).get('stage') == 'parse_bar':
                return
            if live:
                if event:
                    live({"type":"workflow", "event":event})
                # Technical details retain the existing debug feature authorization.
                from feature_flags import feature_available
                allowed_trace = all(feature_available(key, request.current_user or {}) for key in ('debug_execution_trace','ask_field_execution_trace','ask_field_generated_sql'))
                if allowed_trace or (payload.get('event') or {}).get('stage') == 'parse_bar':
                    live(payload)
                else:
                    # Retain raw events for server audit; transport never publishes audit_trace.
                    live({**payload, 'type':'audit_trace'})
        if live:
            live({"type":"workflow", "event":run.record({"type":"started", "status":"running", "catalog":catalog(decision.flow), "activity":{"kind":"intent","heading":"本次分析目标","question":getattr(request,"question","")}})})
        kwargs = dict(allowed_dataset_ids=request.allowed_dataset_ids, live_callback=emit, current_user=request.current_user)
        try:
            with bind_run(run):
                if confirmation:
                    kwargs.update(session_id=request.session_id, selected_option=request.selected_option,
                                  selected_dataset_ids=request.selected_dataset_ids, option_id=request.option_id)
                    if research_confirmation:
                        kwargs['plan_branch_ids'] = request.plan_branch_ids
                    result = service.confirm_by_boss(**kwargs)
                else:
                    kwargs.update(question=request.question, preferred_dataset_ids=request.preferred_dataset_ids,
                                  model_id=request.model_id, session_id=request.session_id,
                                  conversation_history=request.conversation_history)
                    result = service.ask(**kwargs)
                run.check()
            result = self._attach_metadata(result, decision, started)
            result['authorization_scope'] = scope_key(request.current_user or {},request.allowed_dataset_ids)
            outcome = result_outcome(result)
            result['outcome'] = outcome
            if decision.flow == 'basic':
                waiting = bool(result.get('requires_confirmation'))
                good = outcome['status'] in ('completed','empty')
                final_node = 'L3' if waiting else 'L12'
                emit({'event':{'stage':'workflow.final','node_id':final_node,'status':'waiting' if waiting else 'completed' if good else 'warning',
                               'business_summary':outcome['description']}})
                if not waiting and good:
                    emit({'event':{'stage':'workflow.deliver','node_id':'L13','status':'completed','business_summary':'答案与查询依据已交付。'}})
            finished = run.record({'type':'finished','status':outcome['status'],'outcome':outcome})
            if live:
                live({'type':'workflow','event':finished})
            result['workflow'] = {'run_id':run.id, 'flow':decision.flow, 'events':run.events, 'catalog':catalog(decision.flow),
                                  'retry_count':run.retries, 'status':outcome['status'], 'outcome':outcome}
            run.status = result['workflow']['status']
            run.result = result
            return result
        except AskCancelled:
            run.status = 'canceled'
            result = {'aborted':True, 'question':getattr(request,'question',''),
                      'workflow':{'run_id':run.id,'flow':decision.flow,'events':run.events,'status':'canceled'}}
            run.result = result
            return result
        except Exception:
            run.status = 'failed'
            raise

    def ask(self, request: AskRequest) -> Dict[str, Any]:
        return self._execute(request)

    def confirm_by_boss(self, request: ConfirmRequest) -> Dict[str, Any]:
        return self._execute(request, confirmation=True)

    def write_controller_probe(self, payload: Dict[str, Any]) -> None:
        self.basic_service.write_controller_probe(payload)


ask_flow_controller = AskFlowController()
