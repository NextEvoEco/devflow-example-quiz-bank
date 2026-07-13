# V1 Question Bank — Verification

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

1. App loads Question Bank with sidebar + top bar.
2. Empty bank shows empty state (reset DB: delete `data/quiz_bank.db` and restart).
3. Add Question → appears in table with difficulty badge.
4. Search filters by question text.
5. Edit updates the row.
6. Delete confirmation removes the row.
7. Invalid save (empty question text) shows error in modal.
8. Quiz Builder / Online Exam are not present in the V1 sidebar.

## Black-box HTTP check

```bash
curl http://127.0.0.1:5000/api/health
curl http://127.0.0.1:5000/api/questions
```
