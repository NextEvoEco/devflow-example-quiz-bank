# V2 Quiz Builder — Verification

## Startup

Same as V1:

```bash
pip install -r requirements.txt
cd frontend && npm install && npm run build && cd ..
py -m backend
```

Open http://127.0.0.1:5000

## Automated tests

```bash
py -m pytest tests -v
```

## Manual smoke checklist

1. Create at least 3 questions in Question Bank.
2. Open Quiz Builder → New Quiz.
3. Select 3+ questions, reorder with ↑/↓, Preview, Save.
4. Edit and delete quizzes from the list.
5. Saving with fewer than 3 questions shows an error.
