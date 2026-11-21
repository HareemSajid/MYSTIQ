# Testing Report
## Automated (Django test runner) — `python manage.py test tests`
Executed 2026-11-15 in the build sandbox (Python 3.13, offline/demo mode): **Ran 95 tests — 95 passed, 0 failed, 0 skipped** (~65–80 s).
Baseline before this work: 75 tests, all passing. 20 tests added in `tests/test_v2.py`:
retrieval modes (case isolation in dense/bm25/hybrid, unknown mode rejected, cache separation, empty query), nDCG arithmetic, hybrid-vs-dense MRR, off-topic insufficiency, coreference abstention (ambiguous, unambiguous, no antecedent, first person, evaluation precision), settings hardening (refuses placeholder SECRET_KEY with DEBUG=0, accepts real key, no `.env` shipped), strict `transformers` backend failing loudly, prompt-injection not leaking the solution, anonymous/locked-case API access denied, HTML/overlong input safe.
Existing suites cover auth, all seven cases (solve end-to-end), unlocking/progression, RAG, NLI, temporal, NER, stance, leakage and demo-mode behaviour.
The `transformers`-strictness test self-skips if sentence-transformers is installed (it was not installed here, so it ran).

## Not covered by automated tests
- Pretrained model paths (MiniLM embeddings, cross-encoder NLI): **blocked by environment** (HuggingFace unreachable).
- Gemini mode with a real key: not run (no key); the demo/offline path and failure fallbacks are tested.
- Load/performance testing; accessibility audit.

## Browser verification (Playwright/Chromium, scripted, 2026-11-15)
Desktop 1440×900 and mobile 390×844: login; dashboard "next mission" banner; investigation room opens at top (no auto-scroll); body font ≥19 px; tab switching; evidence page and prev/next doc nav; no console/page errors; ask-the-files and hint APIs return grounded answers/hints. Found and fixed: mobile header overflow (nav wider than viewport). Remaining: wide SVG art/tab rail scroll horizontally inside their own containers by design. Not tested: Safari/Firefox, real touch devices, screen readers.
