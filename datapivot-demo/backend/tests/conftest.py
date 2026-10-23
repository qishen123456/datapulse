"""Isolated config and an SDK transport double; tests never contact a model/warehouse."""
import os
from pathlib import Path
import sys
import tempfile
import types

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
_TEST_CONFIG = tempfile.TemporaryDirectory(prefix='datapulse-tests-')
os.environ['DATAPULSE_CONFIG_DIR'] = _TEST_CONFIG.name
try:
    import openai
except ImportError:
    sdk = types.ModuleType('openai')
    class OfflineOpenAI:
        def __init__(self, **kwargs):
            self.base_url = kwargs.get('base_url','')
        def __getattr__(self,name):
            raise RuntimeError('Model transport must be stubbed in isolated tests')
    sdk.OpenAI = OfflineOpenAI
    sys.modules['openai'] = sdk
