import unittest
from analysis_activity import activity_for

class PublicActivityTest(unittest.TestCase):
    def test_aggregation_ignores_literals_comments_and_quoted_names(self):
        event={'stage':'pipeline.agent2_result','sql':"SELECT SUM(volume), 'COUNT(secret)', \"MAX(fake)\" FROM gas /* AVG(x) */ GROUP BY branch"}
        a=activity_for(event)
        self.assertEqual(a['methods'],['SUM'])
        self.assertEqual(a['aggregation'],['按查询维度分组'])
        self.assertNotIn('sql',a)
    def test_only_recorded_result_counts_are_exposed(self):
        self.assertNotIn('row_count',activity_for({'stage':'datasource.execute_sql','status':'response'}))
        a=activity_for({'stage':'datasource.execute_sql','status':'response','row_count':0,'columns':['字段']})
        self.assertEqual((a['row_count'],a['column_count']),(0,1))
    def test_dataset_visibility_policy_applies_to_public_plan(self):
        from ask_projection import project_ask_result
        value={'event':{'activity':{'dataset_name':'internal gas dataset','public_summary':'采用internal gas dataset计算','field_count':64}}}
        projected=project_ask_result(value,{},lambda key,user:key!='ask_field_dataset_hit')
        self.assertEqual(projected['event']['activity']['dataset_name'],'授权数据集')
        self.assertNotIn('public_summary',projected['event']['activity'])
        self.assertEqual(projected['event']['activity']['field_count'],64)

    def test_window_and_distinct_and_public_plan(self):
        a=activity_for({'stage':'pipeline.agent2_result','sql':'SELECT DISTINCT AVG(x) OVER (PARTITION BY branch) FROM gas','public_summary':'比较各分公司平均值'})
        self.assertEqual(a['public_summary'],'比较各分公司平均值')
        self.assertEqual(a['aggregation'],['含窗口计算','含去重处理'])
        self.assertEqual(activity_for({'stage':'pipeline.agent2_result','sql':'SELECT 1','public_summary':'<think>secret'})['public_summary'],'')

if __name__ == '__main__':
    unittest.main()
