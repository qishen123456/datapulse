import unittest
from result_numeric_facts import build_numeric_facts,display

class NumericFactTests(unittest.TestCase):
 def test_exact_unit_rounding(self):
  self.assertEqual(display(1818569)['div_10000_1dp'],'181.9')
  self.assertEqual(display(1420333560)['div_100000000_2dp'],'14.20')
 def test_top_two_share_from_actual_counts(self):
  rows=[{'分公司':n,'新增通气户数':v} for n,v in [('经开',2817),('滨江',2610),('沙湖',1845),('临港',1685),('高新',1520)]]
  fact=build_numeric_facts(rows)['columns'][0]
  self.assertEqual(fact['returned_rows_total']['raw'],'10477')
  self.assertEqual(fact['top_group_shares'][1]['share_of_returned_rows_percent'],'51.80')
 def test_rates_do_not_sum_and_ranking_is_per_measure(self):
  fact=build_numeric_facts([{'分公司':'沙湖','增量_方':1018674,'环比':.0394},{'分公司':'滨江','增量_方':925445,'环比':.0399}])['columns']
  self.assertEqual(fact[0]['maximum_objects'][0]['分公司'],'沙湖')
  self.assertEqual(fact[1]['maximum_objects'][0]['分公司'],'滨江')
  self.assertNotIn('returned_rows_total',fact[1])
 def test_cross_month_balances_not_added(self):
  f=build_numeric_facts([{'month':'2026-08','closing_yuan':10},{'month':'2026-09','closing_yuan':15}])
  self.assertTrue(f['mixed_periods']);self.assertNotIn('returned_rows_total',f['columns'][0])
 def test_no_zero_for_null_or_empty(self):
  self.assertEqual(build_numeric_facts([])['columns'],[])
  f=build_numeric_facts([{'分公司':'输配','安检覆盖率':None}]);self.assertEqual(f['columns'],[])
 def test_signed_changes_have_no_misleading_share(self):
  f=build_numeric_facts([{'变化_方':10},{'变化_方':-20}])['columns'][0]
  self.assertEqual(f['returned_rows_total']['raw'],'-10');self.assertNotIn('top_group_shares',f)

if __name__=='__main__':unittest.main()
