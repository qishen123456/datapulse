import unittest
from types import SimpleNamespace
from ask_runtime import AskRun, bind_run
from llm_client import LLMClient

class TaskFailoverTests(unittest.TestCase):
    def setUp(self):
        self.calls=[]
        self.primary={'id':1,'model':'primary','base_url':'https://primary.invalid/v1','api_key':'fake','api_key_b64':'fake','is_active':True}
        self.backup={'id':2,'model':'backup','base_url':'https://backup.invalid/v1','api_key_b64':'fake','is_active':True}
        def factory(**kw):
            host=kw['base_url']
            def create(**kwargs):
                self.calls.append(kwargs['model'])
                if kwargs['model']=='primary':raise RuntimeError('429 TPM limit reached')
                return 'stream'
            return SimpleNamespace(base_url=host,chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
        self.client=LLMClient(openai_factory=factory,get_default_config=lambda:self.primary,get_configs=lambda:[self.primary,self.backup],decode_secret=lambda x:x,should_retry=lambda e:'429' in str(e),append_trace=lambda *a,**k:None,append_llm_delta=lambda *a,**k:None,extract_json_block=lambda x:x,truncate_text=lambda x,n:str(x)[:n])
        self.client._consume_stream=lambda *args:'AI response'
    def test_successful_fallback_reused_by_later_specialists(self):
        run=AskRun('u','s','basic',{'maxRetries':2})
        with bind_run(run):
            for stage in ['agent2.sql_generate','agent3.sql_review','agent4.analysis']:
                self.assertEqual(self.client._chat('system','user',stage=stage),'AI response')
        self.assertEqual(self.calls,['primary','backup','backup','backup'])
        self.assertEqual(run.retries,1)
    def test_new_task_retries_primary(self):
        for _ in range(2):
            with bind_run(AskRun('u','s','basic',{'maxRetries':2})):self.client._chat('s','u')
        self.assertEqual(self.calls,['primary','backup','primary','backup'])
    def test_no_fallback_when_retry_budget_zero(self):
        with bind_run(AskRun('u','s','basic',{'maxRetries':0})):
            with self.assertRaisesRegex(RuntimeError,'429'):self.client._chat('s','u')
        self.assertEqual(self.calls,['primary'])
    def test_removed_fallback_is_not_reused(self):
        run=AskRun('u','s','basic',{'maxRetries':2})
        with bind_run(run):
            self.client._chat('s','u')
            self.backup['is_active']=False
            with self.assertRaisesRegex(RuntimeError,'无可用模型'):self.client._chat('s','u')
        self.assertEqual(self.calls,['primary','backup'])

if __name__=='__main__':unittest.main()
