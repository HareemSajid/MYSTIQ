import json
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from rag_engine.evaluation import run_all
from rag_engine.report import write_report


class Command(BaseCommand):
    help = "Run the NLP evaluation on data/evaluation/*.json, write results.json and docs/NLP_EVALUATION_REPORT.md."

    def add_arguments(self, parser):
        parser.add_argument("--backend", choices=["auto", "local", "transformers"],
                            help="Override MYSTIQ_NLP_BACKEND. 'transformers' is strict: fails instead of silently falling back.")

    def handle(self, *a, **o):
        if o.get("backend"):
            settings.MYSTIQ["NLP_BACKEND"] = o["backend"]
            from rag_engine.retriever import reset_retrievers
            reset_retrievers()
        res = run_all()
        out = Path(settings.MYSTIQ["EVAL_DIR"]) / "results.json"
        out.write_text(json.dumps(res, indent=1), encoding="utf-8")
        write_report(res)
        r, n = res["retrieval"], res["nli"]
        self.stdout.write(self.style.SUCCESS(
            f"Retrieval P@3={r['precision@3']} nDCG@3={r['ndcg@3']} R@3={r['recall@3']} MRR={r['mrr']} | "
            f"NER F1={res['ner']['mystiq (spaCy + case lexicon + temporal)']['f1']} | Temporal F1={res['temporal']['f1']} | "
            f"Coref acc={res['coreference']['accuracy']} | NLI acc dev={n['dev']['accuracy']} fresh={n['fresh']['accuracy']} | "
            f"Answer eval acc={res['answer_evaluation']['accuracy']}"))
