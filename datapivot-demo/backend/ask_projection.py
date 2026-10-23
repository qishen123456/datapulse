"""Apply console field-visibility policies at the HTTP boundary, after auditing."""
from copy import deepcopy


def project_ask_result(result, user, feature_check=None):
    if feature_check is None:
        from feature_flags import feature_available
        feature_check = feature_available
    flags = {key:feature_check(key,user or {}) for key in (
        'ask_field_execution_trace','ask_field_generated_sql','ask_field_dataset_hit',
        'ask_field_confidence','ask_field_token_usage','ask_field_error_detail')}
    sql_keys = {'sql','final_sql','sql_text','generated_sql','failed_sql','repaired_sql','seed_sql','matched_sample_sql','golden_sql'}
    trace_keys = {'diagnostics','logs','steps','trace','traceback','report_debug','response_text','system_prompt','user_prompt','thought','reasoning_text','reasoning_delta'}
    token_keys = {'token_usage','usage','prompt_tokens','completion_tokens','total_tokens','input_tokens','output_tokens'}
    def visit(value):
        if isinstance(value,list):
            return [visit(item) for item in value]
        if not isinstance(value,dict):
            return value
        output = {}
        for key,item in value.items():
            name = str(key).lower()
            if name == 'rows':
                output[key] = deepcopy(item)
                continue
            if not flags['ask_field_generated_sql'] and (name in sql_keys or name == 'codeblocks'):
                continue
            if (not flags['ask_field_execution_trace'] or not flags['ask_field_generated_sql']) and name in trace_keys:
                continue
            if not flags['ask_field_dataset_hit'] and name == 'public_summary':
                continue
            if not flags['ask_field_confidence'] and name == 'confidence':
                continue
            if not flags['ask_field_token_usage'] and name in token_keys:
                continue
            if not flags['ask_field_dataset_hit'] and name in {'dataset_name','data_source'}:
                output[key] = '授权数据集'
            elif not flags['ask_field_error_detail'] and name == 'error' and item:
                output[key] = '本次查询未完成，请调整问题或联系管理员查看执行记录。'
            else:
                output[key] = visit(item)
        return output
    return visit(deepcopy(result))
