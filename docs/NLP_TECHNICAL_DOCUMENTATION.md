# NLP Technical Documentation
| Component | Technique | Code |
|---|---|---|
| Chunking & preprocessing | per-document/statement/sentence/topic chunks, lemmatised tokens, synonym folding, time tokens `tHHMM` | `rag_engine/preprocess.py`, `chunker` |
| Dense retrieval | Sentence-Transformers all-MiniLM-L6-v2 (enhanced) or TF-IDF + TruncatedSVD (LSA, `random_state=7`) with FAISS inner product, one index per case | `embeddings.py`, `vector_store.py` |
| Lexical retrieval | BM25 (k1=1.5, b=0.75) | `bm25.py` |
| Hybrid ranking | `0.6·dense + 0.4·bm25/max` + bonuses (entity, time ±10 min, document title, focused doc), near-duplicate removal, optional cross-encoder rerank | `retriever.py` |
| Insufficient evidence | top dense < MIN_SCORE **and** BM25 < 2, or zero lexical support under LSA → answer refused/flagged | `retriever.py` |
| Grounded generation | extractive demo answer with citations; Gemini optional; guard blocks culprit/secret leaks and confessions | `generation.py`, `guard.py` |
| NER | spaCy en_core_web_sm + case lexicon (names, titles, roles, objects, places) + temporal extractor | `nlp_engine/ner.py` |
| Temporal | regex/grammar for clock times, "quarter past", "half past", relative terms; AM/PM inference flagged `ambiguous` | `temporal.py` |
| Coreference | spaCy dependency parse + roster; gender agreement, recency, subject salience. **Abstains** when the top two candidate persons differ by < 0.65 score | `coref.py` |
| NLI | symbolic frame engine (actor/predicate/place/time/negation/stance) with comparability gating (same person, day, event window); optional pretrained cross-encoder fused with the gate | `nli.py`, `frames.py` |
| Stance & leakage | rules for observation / assumption / hearsay / denial; leakage checks against private evidence | `stance.py`, `guard.py` |
| Answer evaluation | concept coverage via embedding similarity + culprit-mention penalty (×0.6) → good / partial / poor | `answer_eval.py` |

Design choices: contradiction is only declared when statements are *comparable*; a different-but-compatible pair is neutral. Confidence numbers are heuristics.
Runtime modes: `MYSTIQ_NLP_BACKEND=auto|local|transformers`; the `transformers` option never silently falls back.
