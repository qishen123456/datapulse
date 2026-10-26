"""Permission contract tests without database or external model requests."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import Mock, patch
from flask import Flask, jsonify

class ModelActionPermissions(unittest.TestCase):
    def setUp(self):
        self.allowed=set();self.calls=[]
        config=types.ModuleType('config_manager')
        for name in ['get_ai_models_safe','get_ai_model_by_id','save_ai_model','update_ai_model','delete_ai_model','read_json','write_json']:
            setattr(config,name,Mock(return_value={}))
        config.delete_ai_model.return_value=True
        config.get_ai_model_by_id.return_value={'id':1,'is_default':False}
        config.save_ai_model.return_value={'id':2}
        config.update_ai_model.return_value={'id':1}
        security=types.ModuleType('security')
        def require(key,*args):
            self.calls.append(key)
            return ({'role':'admin'},None) if key in self.allowed else (None,(jsonify(error='denied'),403))
        security.require_feature=require;security.require_login=lambda:({},None)
        vanna=types.ModuleType('vanna_core');vanna.test_ai_model=Mock();vanna.mark_reinit=Mock()
        path=Path(__file__).resolve().parents[1]/'controllers/ai_models.py'
        spec=importlib.util.spec_from_file_location('_test_model_permissions',path)
        mod=importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules,{'config_manager':config,'security':security,'vanna_core':vanna}):spec.loader.exec_module(mod)
        self.config=config;self.app=Flask(__name__);self.app.register_blueprint(mod.ai_models_bp);self.client=self.app.test_client()
    def test_edit_does_not_grant_delete(self):
        self.allowed={'ai_model_edit'}
        self.assertEqual(self.client.delete('/api/ai-models/1').status_code,403)
        self.config.delete_ai_model.assert_not_called()
    def test_edit_does_not_grant_default(self):
        self.allowed={'ai_model_edit'}
        self.assertEqual(self.client.post('/api/ai-models/1/set-default').status_code,403)
        self.assertEqual(self.client.put('/api/ai-models/1',json={'is_default':True}).status_code,403)
        self.config.update_ai_model.assert_not_called()
    def test_create_cannot_bypass_default(self):
        self.allowed={'ai_model_edit'}
        self.assertEqual(self.client.post('/api/ai-models',json={'name':'test','api_key':'fake','is_default':True}).status_code,403)
    def test_channel_permission_is_independent(self):
        self.allowed={'ai_channel_edit'}
        self.assertEqual(self.client.put('/api/ai-models/1',json={'_operation_scope':'channel','base_url':'https://example.invalid/v1'}).status_code,200)
        self.assertEqual(self.client.put('/api/ai-models/1',json={'_operation_scope':'channel','model':'other'}).status_code,400)
        self.assertEqual(self.client.put('/api/ai-models/1',json={'model':'other'}).status_code,403)
    def test_ordinary_edit_still_works(self):
        self.allowed={'ai_model_edit'}
        self.assertEqual(self.client.put('/api/ai-models/1',json={'name':'new name'}).status_code,200)
    def test_explicit_delete_permission(self):
        self.allowed={'ai_model_delete'}
        self.assertEqual(self.client.delete('/api/ai-models/1').status_code,200)
        self.config.delete_ai_model.assert_called_once_with(1)

if __name__=='__main__':unittest.main()
