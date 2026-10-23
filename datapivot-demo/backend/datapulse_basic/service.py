from __future__ import annotations

from typing import Any, Dict
import threading
from ask_runtime import scope_key, owner_key, current_run
from memory.scoped_memory import ScopedMemoryStore
from four_agent_ask import FourAgentAskService

from four_agent_ask import four_agent_ask_service


class BasicAskService:
    """Thin wrapper around the existing four-agent pipeline."""

    name = "basic"

    def __init__(self, delegate=None):
        self.delegate = delegate or four_agent_ask_service
        self._use_request_engines = delegate is None
        self._lock = threading.RLock()

    @property
    def repository(self):
        return self.delegate.repository

    def ask(self, **kwargs) -> Dict[str, Any]:
        if not self._use_request_engines:
            return self.delegate.ask(**kwargs)
        # LLM model/client configuration must not race across simultaneous users.
        engine = FourAgentAskService()
        from datapulse_advanced.config_store import load_config
        engine._skill_config = load_config()
        engine._skill_flow = 'basic'
        if current_run():
            current_run().config['skillPolicy'] = {s['key']: bool(s.get('enabled')) for s in engine._skill_config['skills']}
        engine.short_term_memory = ScopedMemoryStore(self.delegate.short_term_memory, scope_key(kwargs.get('current_user') or {},kwargs.get('allowed_dataset_ids')))
        engine._pending_confirmations = self.delegate._pending_confirmations
        # All ordinary answers require model SQL generation and interpretation.
        # Golden/rule SQL may guide the model but must never bypass it.
        engine._require_ai = True
        result = engine.ask(**kwargs)
        if result.get('requires_confirmation') and result.get('session_id'):
            pending = engine._pending_confirmations.get(result['session_id'])
            if pending is not None:
                pending['_owner'] = owner_key(kwargs.get('current_user') or {})
                pending['_scope'] = scope_key(kwargs.get('current_user') or {},kwargs.get('allowed_dataset_ids'))
                pending['_model_id'] = kwargs.get('model_id')
                pending['_skill_config'] = engine._skill_config
                pending['_retry_count'] = current_run().retries if current_run() else 0
        return result

    def confirm_by_boss(self, **kwargs) -> Dict[str, Any]:
        if not self._use_request_engines:
            return self.delegate.confirm_by_boss(**kwargs)
        user = kwargs.get('current_user') or {}
        session_id = kwargs.get('session_id')
        with self._lock:
            pending = self.delegate._pending_confirmations.get(session_id)
            if not pending or pending.get('_owner') != owner_key(user) or pending.get('_scope') != scope_key(user,kwargs.get('allowed_dataset_ids')):
                return {'error':'确认会话已过期或组织授权已变化，请重新发起问数。'}
            if pending.get('_executing'):
                return {'error':'该确认已在执行，不能重复提交。'}
            pending['_executing'] = True
            model_id = pending.get('_model_id')
            if current_run():
                current_run().retries = pending.get('_retry_count',0)
        engine = FourAgentAskService()
        from datapulse_advanced.config_store import load_config
        engine._skill_config = pending.get('_skill_config') or load_config()
        engine._skill_flow = 'basic'
        if current_run():
            current_run().config['skillPolicy'] = {s['key']: bool(s.get('enabled')) for s in engine._skill_config['skills']}
        engine._require_ai = True
        engine._preferred_model_id = model_id
        engine.short_term_memory = ScopedMemoryStore(self.delegate.short_term_memory, scope_key(kwargs.get('current_user') or {},kwargs.get('allowed_dataset_ids')))
        engine._pending_confirmations = self.delegate._pending_confirmations
        return engine.confirm_by_boss(**kwargs)

    def route_with_agent1(self, *args, **kwargs) -> Dict[str, Any]:
        return self.delegate.route_with_agent1(*args, **kwargs)

    def write_controller_probe(self, payload: Dict[str, Any]) -> None:
        if hasattr(self.delegate, "_write_trace_line"):
            self.delegate._write_trace_line(payload)


basic_ask_service = BasicAskService()
