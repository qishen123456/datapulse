import copy
import unittest
from generate_demo import generate, validate


class ModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tables, cls.orgs, cls.exceptions = generate()

    def test_reproducible_and_reconciled(self):
        self.assertEqual(self.tables, generate()[0])
        self.assertEqual(validate(self.tables, self.orgs, self.exceptions)["status"], "passed")

    def test_business_variability_and_temporal_safety(self):
        from collections import defaultdict
        from datetime import date
        volumes=defaultdict(list)
        for r in self.tables['gas_sales_monthly']:
            volumes[(r['month'],r['branch_id'],r['user_type'])].append(r['volume_m3'])
        self.assertTrue(all(len(set(v))>1 for v in volumes.values()))
        self.assertGreater(len({r['length_km'] for r in self.tables['gas_network_assets']}),100)
        self.assertTrue(any(not r['gis_loaded_date'] for r in self.tables['gas_network_assets']))
        for r in self.tables['gas_safety_monthly']:
            self.assertTrue(0<=r['inspected']<=r['due_inspect'])
            self.assertTrue(0<=r['emergency_on_time']<=r['emergency_total'])
            if r['branch_id']=='GYSP': self.assertEqual(r['due_inspect'],0)
        for r in self.tables['gas_hazard_orders']:
            self.assertLessEqual(r['found_date'],r['as_of_date'])
            self.assertLessEqual(r['found_date'],r['due_date'])
            if r['completed_date']:
                self.assertLessEqual(r['found_date'],r['completed_date'])
                self.assertLessEqual(r['completed_date'],r['as_of_date'])
            if r['severity']=='重大': self.assertLess(r['due_date'],r['as_of_date'])
        recent=[r for r in self.tables['gas_ar_monthly'] if r['month']=='2026-09']
        self.assertTrue(any(r['aging_365_plus_yuan']>0 for r in recent))

    def test_reject_unknown_organization(self):
        tables = copy.deepcopy(self.tables)
        tables["gas_sales_monthly"][0]["org_id"] = "UNKNOWN"
        with self.assertRaises(AssertionError):
            validate(tables, self.orgs, self.exceptions)

    def test_reject_wrong_parent_path(self):
        orgs = copy.deepcopy(self.orgs)
        orgs["nodes"][-1]["parent_id"] = "SHAHU"
        with self.assertRaises(AssertionError):
            validate(self.tables, orgs, self.exceptions)

    def test_reject_broken_receivable(self):
        tables = copy.deepcopy(self.tables)
        tables["gas_ar_monthly"][0]["closing_yuan"] += 100
        with self.assertRaises(AssertionError):
            validate(tables, self.orgs, self.exceptions)

    def test_reject_duplicate_key(self):
        tables = copy.deepcopy(self.tables)
        tables["gas_sales_monthly"].append(tables["gas_sales_monthly"][0])
        with self.assertRaises(AssertionError):
            validate(tables, self.orgs, self.exceptions)


if __name__ == "__main__":
    unittest.main()
