# MYSTIQ — An NLP-driven evidence investigation system
MYSTIQ is an NLP-driven evidence investigation system with an interactive Sherlock-Holmes-style detective interface. Users reason over
seven authored case files using real NLP components: hybrid retrieval-augmented generation (dense + BM25) with citations and
insufficient-evidence handling, natural-language inference with context gating, NER, temporal extraction, coreference with abstention,
epistemic-stance analysis, information-leakage guards and semantic answer evaluation. Every metric in `docs/NLP_EVALUATION_REPORT.md` is
produced by `python manage.py evaluate_nlp`, not typed by hand.

Documentation: [ARCHITECTURE](docs/ARCHITECTURE.md) · [NLP technical](docs/NLP_TECHNICAL_DOCUMENTATION.md) · [Evaluation](docs/NLP_EVALUATION_REPORT.md) ·
[Testing](docs/TESTING_REPORT.md) · [Installation](docs/INSTALLATION_GUIDE.md) · [API](docs/API_DOCUMENTATION.md) · [Limitations](docs/LIMITATIONS_AND_FUTURE_WORK.md)

**Modes.** *Offline/demo* (default, no API, local LSA embeddings + symbolic NLI, clearly labelled in the UI) and *enhanced*
(`pip install sentence-transformers`, optional `GEMINI_API_KEY`). Pretrained models were **not** evaluated in the build environment
(network blocked) — see the evaluation report.

## Quick start (Windows)
1. Install Python 3.10+ (tick "Add to PATH").
2. Double-click **setup.bat**, then **run.bat** → http://127.0.0.1:8000/
(Details, optional pretrained models and Gemini: `docs/SETUP_AND_TESTING.md`.)

## Manual commands
```
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
copy .env.example .env
python manage.py migrate
python manage.py load_cases          # 7 cases from data/cases/*.yaml + NLP-built timelines
python manage.py build_index         # chunk → embed → per-case FAISS indexes
python manage.py runserver
python manage.py test tests          # automated tests
python manage.py evaluate_nlp        # metrics + docs/NLP_EVALUATION_REPORT.md
```

## The seven cases
1 The Missing Emerald (observation vs assumption) · 2 The Midnight Letter (information leakage) · 3 The Locked Library (timeline, false contradiction) ·
4 The Vanishing Passenger (reference resolution) · 5 The Clockmaker's Secret (literally true but misleading) · 6 The Poisoned Invitation (cross-document entities; non-operational) ·
7 The Final Deception (three independent proofs required).

## Modes (stated honestly in the UI and API)
* **Embeddings/NLI:** pretrained Sentence-Transformers models when installed; otherwise local fallbacks (LSA embedder, symbolic NLI). `/api/status/` shows which are active.
* **Generation:** Gemini when `GEMINI_API_KEY` is set; otherwise a grounded, extractive **demo mode**. Suspect demo answers come from authored, retrieved interview topics — never invented.

## Layout
`config/ accounts/ cases/ game/ rag_engine/ nlp_engine/ templates/ static/ data/{cases,evaluation}/ vector_store/ tests/ docs/`

## Documentation
`docs/ARCHITECTURE.md` · `docs/SETUP_AND_TESTING.md` · `docs/NLP_EVALUATION_REPORT.md`

## Known limitations
See the report's section 9. Notably: the symbolic NLI is tuned to the vocabulary of these cases; evaluation datasets are small; coreference is heuristic;
the UI was verified with server-side tests and scripted Chromium (Playwright) checks on desktop and mobile widths (see docs/TESTING_REPORT.md); no manual cross-browser or screen-reader testing.


## UI redesign (v2)
Design identity: **Victorian Detective Editorial / Premium Mystery Archive** — see `docs/design_system.html` and `docs/MYSTIQ_UI_Redesign_All_Screens.pdf` (all screens).
* **Seven cases = seven visual themes** (`game/themes.py`, `[data-case=N]` in `static/css/mystiq.css`): Emerald Noir, Midnight Correspondence, Gothic Archive, Railway Mystery, Clockwork Noir, Poisoned Elegance, The Last Conspiracy — each with its own palette, pattern and original cover artwork (`templates/game/art/`, regenerate with `python tools/gen_art.py`).
* **One system**: Cormorant Garamond / Newsreader / IBM Plex Mono (bundled, offline), one masthead + case bar + stage tracker, one spacing scale, one component set.
* **Eight NLP instruments** have fixed icons/colours in every case (retrieval, NLI, NER, temporal, coreference, stance, leakage, evaluation).
* Documents render as their own paper type (letter, telegram, ledger, newspaper, diary, blueprint plan, receipt, typed record) instead of one parchment.
* Suspect portraits are procedural *illustrated* portraits (age, gender, role-based attire, facial hair, hair) — stylised, not photographic; deterministic and never case-solution dependent.
* Backend, URLs, API and tests are unchanged (75 tests pass).
