# API Documentation
All endpoints require a logged-in session and the CSRF header (`X-CSRFToken`); JSON in, JSON out. A case that is locked for the user returns 403/404/redirect.
Evidence is isolated per case (separate FAISS index per case, case number checked on every result).

| Method & path | Body | Response (main fields) |
|---|---|---|
| GET `/api/status/` | – | backend info: embedder, NLI backend, spaCy, Gemini configured, mode (demo/enhanced) |
| POST `/api/case/<n>/ask/` | `{question (≤500 chars), doc_key?}` | `answer`, `citations[]`, `insufficient`, `mode`, `confidence_note` |
| POST `/api/case/<n>/watson/` | `{question}` | hint-style guidance; never reveals the culprit |
| POST `/api/case/<n>/hint/` | – | `{order, text, hints_used, hints_total}`; `{error:"no_more_hints"}` when exhausted |
| POST `/api/case/<n>/interrogate/` | `{suspect, question (≤400), present?}` | in-character `answer`, `stance`, citations; no confessions/secrets (guard) |
| POST `/api/case/<n>/explain/` | `{statement_id}` | stance, entities, times, coreference (incl. `abstained`), leakage flags |
| POST `/api/case/<n>/compare/` | `{a, b}` statement ids | NLI `label`, `confidence`, `finding`, `rationale[]`, `backend`, comparability gates |
| GET `/api/case/<n>/evidence/<key>/analysis/` | – | per-document NLP analysis |
| POST `/api/case/<n>/important/` | `{doc_key}` | toggle flag → `{important, count}` |
| POST `/api/case/<n>/notebook/` | `{text ≤8000}` | `{saved:true}` |

Errors: 400 `{error}` for empty/short input; 404 unknown statement/document. `confidence` values are heuristic scores, **not** calibrated probabilities.
Retrieval (internal) accepts `mode=hybrid|dense|bm25`; used by the evaluation harness.
