# MYSTIQ — NLP Evaluation Report
Generated 2026-11-15 (seed 7, requested backend `auto`) by `python manage.py evaluate_nlp`. All numbers below were computed by that command from the labelled files in `data/evaluation/`.

## 1. Environment (which models produced these numbers)
| Component | Backend used in this run |
|---|---|
| Embeddings / retrieval | `local-lsa-tfidf` |
| NLI | symbolic frame-based engine + gating (pretrained NLI model not loaded: ModuleNotFoundError: No module named 'sentence_transformers') |
| spaCy | `en_core_web_sm` |
| LLM generation | Not used (demo mode); the evaluation measures retrieval/NLP, not generated prose |

**Important:** if the row above says `local-lsa-tfidf`, the pretrained Sentence-Transformers model was NOT available in the environment that ran this evaluation. A pretrained transformer is expected to retrieve paraphrased queries better than the local LSA fallback. Re-run `python manage.py build_index` and `python manage.py evaluate_nlp` after `pip install sentence-transformers` to get the pretrained numbers on your machine.

## 2. Retrieval (56 labelled queries, document-level relevance; `dev` = 32 queries written while building, `fresh` = 24 written afterwards)
Ablation (K=3; P@K/R@K/nDCG@K computed over documents, duplicate chunks of one document collapsed):

| Mode | Subset | n | P@3 | R@3 | nDCG@3 | MRR | Hit@1 |
|---|---|---|---|---|---|---|---|
| dense | dev | 32 | 0.323 | 0.828 | 0.741 | 0.764 | 0.625 |
| dense | fresh | 24 | 0.375 | 0.979 | 0.923 | 0.91 | 0.833 |
| dense | all | 56 | 0.345 | 0.893 | 0.819 | 0.826 | 0.714 |
| bm25 | dev | 32 | 0.312 | 0.781 | 0.764 | 0.827 | 0.75 |
| bm25 | fresh | 24 | 0.375 | 0.979 | 0.919 | 0.896 | 0.792 |
| bm25 | all | 56 | 0.339 | 0.866 | 0.83 | 0.856 | 0.768 |
| hybrid | dev | 32 | 0.344 | 0.859 | 0.793 | 0.826 | 0.719 |
| hybrid | fresh | 24 | 0.375 | 0.979 | 0.95 | 0.938 | 0.875 |
| hybrid | all | 56 | 0.357 | 0.911 | 0.86 | 0.874 | 0.786 |

Headline (hybrid, all queries): P@3 0.357, R@3 0.911, nDCG@3 0.86, MRR 0.874, Hit@1 0.786, Hit@5 1.

| Check | Value |
|---|---|
| Case isolation (no cross-case chunk in any result, all three modes) | True |
| Off-topic queries correctly flagged "insufficient evidence" | 8/8 |
| Legitimate queries wrongly flagged "insufficient" | 0/56 |
| Hybrid latency mean / p50 / p95 (ms) | 10.8 / 10.1 / 15.0 |

`dense` and `bm25` modes are pure single-signal rankings; `hybrid` additionally applies the entity/time/title bonuses. Hybrid therefore differs from the others in two ways (fusion AND reranking bonuses); this ablation does not separate those two effects.

Queries whose relevant document was not in the top 3 (hybrid):
- query: Who last held the emerald before it was locked away? | relevant: ['lord_note'] | got: ['', 'eleanor_statement', 'study_report', 'lord_note', 'message']
- query: Who kept asking where Blackwood would be on Friday? | relevant: ['diary'] | got: ['helen_statement', 'delivery_record', 'police_notice', 'diary', '']
- query: Who sat at the foot of the table? | relevant: ['seating'] | got: ['hale_statement', 'mills_statement', 'service_record', 'seating', '']

Most queries have exactly one relevant document, so P@3 is bounded by 1/3 (= 0.333) even for perfect retrieval; read R@3, nDCG@3 and MRR for quality.

## 3. Named Entity Recognition (2 systems compared on 15 labelled sentences, exact span+label match)
| System | Precision | Recall | F1 | ms/sentence |
|---|---|---|---|---|
| MYSTIQ (spaCy + case lexicon + temporal extractor) | 0.963 | 0.981 | 0.972 | 4.3 |
| Baseline (spaCy only) | 0.706 | 0.453 | 0.552 | 3.8 |

Per-label recall (MYSTIQ): {'DATE': '3/3', 'LOCATION': '11/11', 'OBJECT': '9/9', 'ORGANISATION': '0/1', 'OTHER': '1/1', 'PERSON': '17/17', 'TIME': '11/11'}

## 4. Temporal extraction (27 items)
Precision 1.0, Recall 1.0, F1 1.0 (time values normalised to HH:MM). Ambiguity-flag accuracy: 2/2. Mean latency 0.03 ms.

Errors:
_none_

## 5. Coreference / reference resolution (with abstention)
| Subset | Pronouns | Accuracy | Precision when resolving | Coverage | Abstentions (correct) |
|---|---|---|---|---|---|
| dev | 12 | 0.917 | 1.0 | 0.917 | 1 (0) |
| fresh | 6 | 1.0 | 1.0 | 0.5 | 3 (3) |
| all | 18 | 0.944 | 1.0 | 0.778 | 4 (3) |

Accuracy counts an abstention as correct only when the gold answer is "ambiguous (None)". The ambiguity margin was set after looking at the fresh items, and the fresh set is only 6 pronouns, so treat it as a demonstration of behaviour, not a benchmark.
- text: Dr. Moore saw Carter in the library. He was putting away the case. | pronoun: He | expected: carter | got: None | abstained: True

## 6. Natural language inference with context gating
Backend: symbolic-frames+gating. Mean latency 7.4 ms (p95 20.2 ms).

| Subset | n | Accuracy | False contradictions |
|---|---|---|---|
| dev (pairs used while building the rules — optimistic) | 13 | 1.0 | 0 |
| fresh (first run scored 0.667 = 10/15 before I used its errors to repair rules, so it is NO LONGER unbiased) | 15 | 1.0 | 0 |
| **heldout** (written last; never used to tune anything — the honest estimate) | 12 | **0.833** | 0 |
| all | 40 | 0.95 | 0 |

Per-class (all): contradiction: P=1.0 R=0.947 F1=0.973, entailment: P=1.0 R=0.5 F1=0.667, neutral: P=0.905 R=1.0 F1=0.95

A *false contradiction* (predicting contradiction for a pair whose gold label is not contradiction) is the most harmful error in this game, because it would send the player after an innocent suspect.

Errors on the held-out set:
- premise: I was in the estate office until ten. | hypothesis: Miss Grey was seen in the estate office at 9:30 PM. | gold: entailment | pred: neutral | finding: no_relation
- premise: I never set foot in the workshop. | hypothesis: Captain Finch entered the workshop at 8:20 PM. | gold: contradiction | pred: neutral | finding: no_relation

## 7. Semantic answer evaluation (14 labelled explanations: good vs. poor)
Accuracy 1.0.


## 8. End-to-end latency (demo mode, no external LLM)
Ask-the-case-files mean 116.2 ms; suspect interrogation mean 13.2 ms. A Gemini call would add its own network latency, which was not measured.

## 9. Limitations (honest)
- The datasets are small (tens of items) and written by the project author; the metrics are indicative, not statistically strong.
- The symbolic NLI engine is rule-based and tuned to the vocabulary of the seven cases; it will not generalise to arbitrary text. The pretrained NLI cross-encoder (when installed) is fused with the same context gating.
- Temporal AM/PM is inferred; such times are flagged `ambiguous`.
- Coreference is heuristic. NER uses spaCy's small model plus a case lexicon, so unseen names depend on spaCy alone.
- Offline demo mode answers are *extractive*: with the local embedder they sometimes quote a less central sentence of the right document (the citations still lead to it). A pretrained embedding model or Gemini gives better answers.
- The `what`/`when` multiple-choice options in the final deduction are written per case; a very careful reader can sometimes infer the culprit from their wording.
- No claim is made of perfect accuracy.
