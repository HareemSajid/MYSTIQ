# Limitations and Future Work
## Limitations (measured or known)
- **Pretrained models not evaluated.** The build sandbox could not reach HuggingFace, so all numbers use the local LSA embedder and symbolic NLI. Pretrained results must be produced on the user's machine (`evaluate_nlp --backend transformers`).
- Datasets are small and author-written: retrieval 56 queries, NER 15 sentences, temporal 27, coreference 18 pronouns, NLI 40 pairs (held-out 12, with only 2 entailment items), answer evaluation 14. Metrics are indicative, not statistically strong; no confidence intervals.
- Several "fresh" sets were authored after the system was tuned and some were used for repair (NLI "fresh" explicitly); only NLI `heldout` was never used for tuning. The coreference margin (0.65) was chosen after seeing the 6 fresh items.
- Hybrid-vs-single-signal ablation mixes fusion with heuristic bonuses.
- Symbolic NLI is tuned to the vocabulary of the 7 cases and will not generalise.
- Demo-mode answers are extractive and can quote a less central sentence; citations still point to the right document.
- Coreference coverage drops when it abstains (e.g. 0.78 overall) — by design.
- Mission progress (XP/ticks) lives in browser localStorage, per browser.
- Not load-tested; SQLite only.
## Future work
Evaluate MiniLM + cross-encoder NLI on a larger, independently labelled set (e.g. add MNLI-style pairs); learn fusion weights on a validation split; bootstrap confidence intervals; calibrate confidence; user study of the UI.
