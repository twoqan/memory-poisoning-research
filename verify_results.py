#!/usr/bin/env python3
"""Offline checks for paired experiments; makes no network or paid model calls."""
import json
from pathlib import Path
from collections import Counter

BASE=Path(__file__).resolve().parent
for version in ('v4_1', 'v5'):
    rows_by_model={}
    for prefix, label in [('ollama_qwen3_8b','Qwen3 8B'),('openai_gpt-4.1-mini','GPT-4.1 mini')]:
        path=BASE/'data'/version/f'{prefix}_{version}.jsonl'
        rows=[json.loads(line) for line in path.read_text(encoding='utf8').splitlines() if line.strip()]
        assert len(rows)==200,(version,label,'row_count',len(rows))
        keyed={(r['case_id'],r['orientation'],r['condition'],r['repeat']):r for r in rows}
        assert len(keyed)==200,(version,label,'duplicates')
        assert all(r['error'] is None and r['valid_json'] for r in rows),(version,label,'invalid/error')
        rows_by_model[label]=keyed
        cond=Counter((r['condition'],r['correct_decision']) for r in rows)
        print(version, label, 'correct',sum(r['correct_decision'] for r in rows),'/200', 'wrong',sum(r['wrong_decision'] for r in rows))
        for c in ('clean','untrusted_first','trusted_first','trust_instruction','filtered'):
            print(' ',c,cond[c,True],'/40')
    q=rows_by_model['Qwen3 8B'];g=rows_by_model['GPT-4.1 mini']
    assert q.keys()==g.keys()
    for k in q:
        assert (q[k]['system_prompt'],q[k]['user_prompt'],q[k]['expected'])==(g[k]['system_prompt'],g[k]['user_prompt'],g[k]['expected']),('prompt mismatch',k)
    pairs=Counter((q[k]['correct_decision'],g[k]['correct_decision']) for k in q)
    print(' paired:',dict(pairs))
print('PASS: 800 valid rows, paired prompts and expected decisions verified.')
