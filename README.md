# Memory Poisoning: Controlled Read-Time Memory Conflicts

**Turkish Medium research companion** · Qwen3 8B (Ollama) vs GPT-4.1 mini (OpenAI Responses API)

This repository contains the Python experiment code, reproducible input datasets, **800 recorded decisions** (200 per model in each of V4.1 and V5), manifests, charts and methodology notes behind the article [Memory Poisoning: Yapay Zekânın Hatıraları Manipüle Edilebilir mi?](articles/medium_tr.md).

**Important scope:** These experiments evaluate *read-time* choices between pre-seeded conflicting records. They **do not** demonstrate a write-time poisoning attack, autonomous long-term-memory compromise, or a general security benchmark. `filtered` is deterministic application-side record removal, so its prompts are identical to `clean`.

## Main results

| Version | Qwen3 8B | GPT-4.1 mini |
| --- | ---: | ---: |
| V4.1 — security policies | 150/200 (75.0%) | 194/200 (97.0%) |
| V5 — neutral fictional UI policies | 149/200 (74.5%) | 196/200 (98.0%) |

V5 conflicting-record conditions only (excluding `clean` and `filtered`): **69/120** vs **116/120** correct, respectively. Tests are **paired**, not 800 independent attacks; each case–orientation–condition was run once per model. Model decoding behavior and hosting environments are not perfectly matched. Correctness measures agreement with the designated `approved_policy`, not real-world security desirability.

## Repository layout

```text
experiments/v4_1/  # Original V4.1 runner, base API client, cases
experiments/v5/    # V5 runner, base API client, cases, summary and tests
data/v4_1/         # 400 V4.1 JSONL rows + 2 manifests
data/v5/          # 400 V5 JSONL rows + 2 manifests
figures/           # Publication graphics (.png/.svg)
docs/              # Reproduction notes, data dictionary
articles/          # Turkish Medium draft
verify_results.py  # Offline audit and pairing checks
```

## Verify published numbers (no API calls)

Requires Python 3.10+; no third-party libraries:

```bash
python3 verify_results.py
```

## Rerun experiments (optional)

V5: from the repository root:

```bash
cd experiments/v5
python3 -m unittest -v test_v5.py
python3 lab_v5.py --backend ollama --model qwen3:8b --repeats 1
```

The local backend requires Ollama and a downloaded `qwen3:8b` model. For OpenAI, set `OPENAI_API_KEY` in the environment **without committing it**; API calls incur charges:

```bash
python3 lab_v5.py --backend openai --model gpt-4.1-mini --repeats 1
```

V4.1 uses `experiments/v4_1/lab_v4_1.py` and its own adjacent `cases.json` and `lab_base.py`:

```bash
cd experiments/v4_1
python3 lab_v4_1.py --backend ollama --model qwen3:8b --repeats 1
```

Existing result files in `data/` are not modified by these commands. Runtime output defaults to each experiment's `results/`, which is ignored by Git.

## Safety, interpretation and publication

- Input records are controlled synthetic records, not text obtained by compromising a live system.
- Reversed policy orientations are **counterfactual controls**, not recommended production settings.
- The two input orders and trust-rule condition probe source ordering and instruction framing, not proof of causal mechanisms.
- JSONL public exports preserve task prompts, decisions, model metadata and token counts; **OpenAI response IDs were removed** prior to public packaging.
- Never commit API keys, `.env` files, personal details, real production policies, or secrets. Inspect every file before publishing.
- Consult [`docs/TEKRARLANABILIRLIK.md`](docs/TEKRARLANABILIRLIK.md) and [`docs/VERI_SOZLUGU.md`](docs/VERI_SOZLUGU.md).

## License

- **Source code:** MIT License — see [LICENSE](LICENSE).
- **Research articles, figures, datasets and documentation:** Creative Commons Attribution 4.0 International — see [LICENSE-CONTENT.md](LICENSE-CONTENT.md).

Copyright © 2026 Tuğkan Türk.

See the respective license files for usage and attribution requirements.
