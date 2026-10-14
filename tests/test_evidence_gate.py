import copy, json, unittest
from pathlib import Path
from src.check_portfolio import check

class EvidenceGate(unittest.TestCase):
    def setUp(self):
        self.spec=json.loads((Path(__file__).resolve().parents[1]/'data/example_portfolio.json').read_text())
    def test_reviewed_example(self):
        self.assertEqual(check(self.spec)['safe_days'],91)
    def test_unknown_not_zero_or_complete(self):
        self.spec['paths'][0]['permissions'][0]['windows']=None
        result=check(self.spec)
        self.assertEqual(result['status'],'unresolved')
        self.assertNotIn('safe_days',result)
    def test_scope_and_handoff_gates(self):
        self.spec['paths'][0]['scope_reviewed']=False
        self.assertEqual(check(self.spec)['status'],'unresolved')
        self.spec['paths'][0]['scope_reviewed']=True
        self.spec['switching']=True
        self.assertEqual(check(self.spec)['status'],'unresolved')

if __name__=='__main__':unittest.main()
