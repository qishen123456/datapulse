"""Request-scoped execution control shared by both independent ask paths.

Cancellation is cooperative at tool boundaries. Active DB connections register a
cancel hook where the driver supports it; no claim of instant model cancellation.
"""
from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from copy import deepcopy
from dataclasses import dataclass, field
from hashlib import sha256
import json
import re
import threading
import time
from typing import Any
from uuid import uuid4


class AskCancelled(RuntimeError):
    pass


def owner_key(user: dict) -> str:
    value = user.get('id') or user.get('user_id') or user.get('username') or user.get('login_account') or user.get('account') or user.get('permission_identifier') or user.get('phone') or user.get('open_id') or user.get('union_id')
    if value is None or str(value).strip() == '':
        raise PermissionError('登录身份无效，无法创建问数任务。')
    return str(value)


def scope_key(user: dict, datasets) -> str:
    # All user attributes participate, including org node ids and custom roles.
    from config_manager import read_json
    policy = [read_json('data_permissions.json'), read_json('organization_trees.json')]
    payload = json.dumps([user, sorted(int(x) for x in datasets or []), policy], sort_keys=True, default=str)
    return sha256(payload.encode()).hexdigest()


@dataclass
class AskRun:
    owner: str
    scope: str
    flow: str
    config: dict
    id: str = field(default_factory=lambda: uuid4().hex)
    created: float = field(default_factory=time.time)
    cancelled: threading.Event = field(default_factory=threading.Event)
    lock: Any = field(default_factory=threading.RLock)
    events: list = field(default_factory=list)
    hooks: list = field(default_factory=list)
    result: dict | None = None
    status: str = 'running'
    sequence: int = 0
    retries: int = 0

    def check(self):
        if self.cancelled.is_set():
            raise AskCancelled('已停止本轮问数，后续工具不会继续执行。')

    def claim_retry(self) -> bool:
        self.check()
        with self.lock:
            limit = min(2, max(0, int(self.config.get('maxRetries', 2))))
            if self.retries >= limit:
                return False
            self.retries += 1
            return True

    def record(self, event: dict) -> dict:
        with self.lock:
            from datetime import datetime, timezone
            self.sequence += 1
            event = {**event, 'run_id': self.id, 'seq': self.sequence, 'flow': self.flow,
                     'time':event.get('time') or datetime.now(timezone.utc).isoformat()}
            # Bounded event history; never persist model reasoning as business progress.
            self.events.append(event)
            self.events = self.events[-300:]
            return event

    def cancel(self):
        self.cancelled.set()
        with self.lock:
            self.status = 'cancel_requested'
            for hook in list(self.hooks):
                try:
                    hook()
                except Exception:
                    pass


_CURRENT = ContextVar('ask_run', default=None)
_RUNS: dict[str, AskRun] = {}
_LOCK = threading.RLock()
_CANCEL_INTENTS = {}


def create_run(user, datasets, flow, config, execution_id=""):
    run = AskRun(owner_key(user), scope_key(user, datasets), flow, deepcopy(config))
    if execution_id:
        if not re.fullmatch(r'[a-f0-9]{32}',str(execution_id)):
            raise ValueError('任务标识格式无效。')
        run.id = execution_id
    with _LOCK:
        if run.id in _RUNS:
            raise ValueError('任务已存在，禁止重复派发。')
        intent = _CANCEL_INTENTS.pop((run.owner,run.scope,run.id),None)
        if intent and time.time()-intent < 30:
            run.cancel()
        expired = [key for key, item in _RUNS.items() if time.time() - item.created > 3600 and item.status != 'running']
        for key in expired:
            del _RUNS[key]
        if len(_RUNS) >= 500:
            raise RuntimeError('问数任务队列已满，请稍后重试。')
        _RUNS[run.id] = run
    return run


def get_run(run_id, user, datasets):
    with _LOCK:
        run = _RUNS.get(run_id)
    if run is None or time.time()-run.created > 3600:
        raise LookupError('任务已过期或服务已重启，请重新发起问数。')
    if run.owner != owner_key(user) or run.scope != scope_key(user, datasets):
        raise PermissionError('当前身份或组织授权已变化，不能访问该任务。')
    return run


def request_cancel(run_id,user,datasets):
    if not re.fullmatch(r'[a-f0-9]{32}',str(run_id)):
        raise LookupError('任务标识无效。')
    try:
        run = get_run(run_id,user,datasets)
    except LookupError:
        # A user can stop immediately, before the SSE worker has registered.
        with _LOCK:
            now = time.time()
            for key,created in list(_CANCEL_INTENTS.items()):
                if now-created > 30:
                    _CANCEL_INTENTS.pop(key,None)
            if len(_CANCEL_INTENTS) >= 1000:
                raise RuntimeError('取消队列已满，请稍后重试。')
            _CANCEL_INTENTS[(owner_key(user),scope_key(user,datasets),run_id)] = now
        return 'cancel_requested'
    if run.status in ('running','cancel_requested'):
        run.cancel()
    return run.status


def current_run():
    return _CURRENT.get()


def checkpoint():
    run = current_run()
    if run:
        run.check()


@contextmanager
def bind_run(run):
    token = _CURRENT.set(run)
    try:
        checkpoint()
        yield run
    finally:
        _CURRENT.reset(token)


@contextmanager
def database_operation(connection):
    run = current_run()
    checkpoint()
    hook = getattr(connection, 'cancel', None) or getattr(connection, 'interrupt', None)
    if run and hook:
        with run.lock:
            run.hooks.append(hook)
        # Close race between the first check and hook registration.
        if run.cancelled.is_set():
            try:
                hook()
            finally:
                checkpoint()
    try:
        yield
        checkpoint()
    finally:
        if run and hook:
            with run.lock:
                if hook in run.hooks:
                    run.hooks.remove(hook)
