# Installation Guide
Requires Python 3.10+ (tested on 3.13).

```
python -m venv venv && source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
cp .env.example .env                                   # Windows: copy .env.example .env
python manage.py migrate
python manage.py load_cases
python manage.py build_index
python manage.py runserver                             # http://127.0.0.1:8000/
```
Windows: `setup.bat` then `run.bat` do the same.

## Configuration (`.env`)
| Variable | Meaning |
|---|---|
| `DJANGO_SECRET_KEY` | **Required when `DJANGO_DEBUG=0`**; the app refuses to start with the default/placeholder key. |
| `DJANGO_DEBUG` | `1` (default, development) / `0` (production). |
| `DJANGO_ALLOWED_HOSTS` | comma-separated hosts. |
| `DJANGO_HTTPS=1` | with DEBUG=0, marks session/CSRF cookies Secure. |
| `GEMINI_API_KEY` | optional; empty = demo mode. Never commit it. |
| `MYSTIQ_NLP_BACKEND` | `auto` (try pretrained, fall back and say so), `local` (never load pretrained), `transformers` (strict: error if the model cannot load). |

## Enhanced mode
`pip install sentence-transformers`, then `python manage.py build_index` (re-embeds with all-MiniLM-L6-v2) and
`python manage.py evaluate_nlp --backend transformers`. With `transformers` the run fails loudly instead of silently falling back.
`/api/status/` and the evaluation report state which backend was actually used.

## Tests / evaluation
`python manage.py test tests` · `python manage.py evaluate_nlp [--backend local|auto|transformers]`
