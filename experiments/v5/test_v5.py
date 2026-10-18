import tempfile
import unittest
import json
from pathlib import Path
from lab_v5 import load_cases, build_prompts, run, CONDITIONS

class V5Tests(unittest.TestCase):
    def test_dataset(self):
        cases=load_cases()
        self.assertEqual(len(cases),20)
        self.assertTrue(all('security' not in x['feature'] for x in cases))

    def test_prompts_and_orientation(self):
        first=load_cases()[0]
        for orientation in ('original','reversed'):
            for condition in CONDITIONS:
                system,user,records,expected=build_prompts(first,orientation,condition)
                self.assertEqual(bool(any(not x['trusted'] for x in records)),condition not in ('clean','filtered'))
                self.assertEqual(' Kaynak güveni kuralı:' in system,condition=='trust_instruction')
                self.assertIn(first['feature'],user)
                self.assertIn(expected, ('ENABLE','DISABLE'))

    def test_mock_pilot(self):
        def caller(backend,model,system,user):
            # Deterministic mock tests only plumbing, not actual model quality.
            marker='ETKİN olmalıdır.'
            trusted=[line for line in user.splitlines() if 'source=approved_policy;' in line][0]
            expected='ENABLE' if marker in trusted else 'DISABLE'
            return json.dumps({'decision':expected}), {'mock':True}
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'pilot.jsonl'
            run('ollama','mock-only',1,out,limit_cases=2,caller=caller)
            rows=[json.loads(s) for s in out.read_text().splitlines()]
            self.assertEqual(len(rows),20)
            self.assertTrue(all(r['correct_decision'] for r in rows))
            self.assertTrue(out.with_suffix('.manifest.json').exists())
            with self.assertRaises(FileExistsError):
                run('ollama','mock-only',1,out,limit_cases=2,caller=caller)

if __name__=='__main__':unittest.main()
