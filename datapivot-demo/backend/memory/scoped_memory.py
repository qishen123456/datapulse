"""Keep client conversation ids within the current user's authorization scope."""
class ScopedMemoryStore:
    def __init__(self, store, namespace):
        self.store = store
        self.namespace = namespace

    def _key(self, session_id):
        return f'{self.namespace}:{session_id}' if session_id else ''

    def get(self, session_id):
        return self.store.get(self._key(session_id))

    def remember_result(self, session_id, *args, **kwargs):
        return self.store.remember_result(self._key(session_id), *args, **kwargs)

    def remember_confirmation(self, session_id, *args, **kwargs):
        return self.store.remember_confirmation(self._key(session_id), *args, **kwargs)

    def resolve_followup(self, *args, **kwargs):
        return self.store.resolve_followup(*args, **kwargs)
