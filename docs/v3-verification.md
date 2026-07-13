# V3 Online Exam — Verification

## Startup

```bash
pip install -r requirements.txt
cd frontend && npm install && npm run build && cd ..
py -m backend
```

Open http://127.0.0.1:5000

## Automated tests

```bash
py -m pytest tests -v
cd frontend && npm test
```

## Manual smoke checklist

1. Ensure a quiz with ≥3 questions exists.
2. Online Exam → Start Exam.
3. Answer questions (prev/next), Submit.
4. Review score ring + answer review.
5. Retry Quiz and Back to Exams.
6. Confirm abandoned attempts (Exit without submit) are not scored.

## Black-box HTTP smoke

```bash
curl http://127.0.0.1:5000/api/health
curl http://127.0.0.1:5000/api/quizzes
```
