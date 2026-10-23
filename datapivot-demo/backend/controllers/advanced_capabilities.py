from __future__ import annotations

from typing import Any, Dict

from flask import Blueprint, jsonify, request

from auth_store import get_current_user
from security import require_feature
from ask_flow.controller import AskFlowController
from datapulse_advanced.config_store import import_skills, load_config, reset_config, save_config
from datapulse_advanced.registry import capability_summary


advanced_capabilities_bp = Blueprint(
    "advanced_capabilities",
    __name__,
    url_prefix="/api/admin/advanced-capabilities",
)


def _require_admin(feature="advanced_capabilities"):
    user = get_current_user()
    if user.get("role") not in {"super_admin", "admin"}:
        return None, (jsonify({"success": False, "error": "只有管理员可以维护技能与工具"}), 403)
    _, denied = require_feature(feature, "当前账号未开放此技能配置操作")
    if denied:
        return None, denied
    return user, None


def _response(config: Dict[str, Any], operator: str = ""):
    flow = AskFlowController().load_config()
    return jsonify(
        {
            "success": True,
            "data": {
                "config": config,
                "summary": capability_summary(config),
                "operator": operator,
                "entryPolicy": {key: flow.get(key) for key in ("advancedEnabled", "defaultFlow")},
            },
        }
    )


@advanced_capabilities_bp.route("", methods=["GET"])
def get_advanced_capabilities():
    _, error = _require_admin()
    if error:
        return error
    config = load_config()
    return _response(config)


@advanced_capabilities_bp.route("", methods=["PUT"])
def update_advanced_capabilities():
    user, error = _require_admin("advanced_capability_save")
    if error:
        return error
    payload = request.get_json(silent=True) or {}
    raw_config = payload.get("config") if isinstance(payload.get("config"), dict) else payload
    config = save_config(raw_config)
    return _response(config, operator=user.get("username") or user.get("name") or "")


@advanced_capabilities_bp.route("/skills/import", methods=["POST"])
def import_advanced_skills():
    user, error = _require_admin("advanced_skill_import")
    if error:
        return error
    payload = request.get_json(silent=True) or {}
    report = import_skills(payload.get("manifest") if isinstance(payload.get("manifest"), (dict, list)) else payload)
    response = {
        "success": True,
        "data": {
            "config": report.get("config") or load_config(),
            "summary": capability_summary(report.get("config") or load_config()),
            "imported": report.get("imported") or [],
            "skipped": report.get("skipped") or [],
            "operator": user.get("username") or user.get("name") or "",
        },
    }
    return jsonify(response)


@advanced_capabilities_bp.route("/reset", methods=["POST"])
def reset_advanced_capabilities():
    user, error = _require_admin("advanced_capability_reset")
    if error:
        return error
    config = reset_config()
    return _response(config, operator=user.get("username") or user.get("name") or "")
