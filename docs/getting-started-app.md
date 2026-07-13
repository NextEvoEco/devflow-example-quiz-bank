# Quiz Bank — Local Startup

## Prerequisites

- Python 3.13+
- Node.js 24+ / npm 11+

## Install

```bash
pip install -r requirements.txt
cd frontend
npm install
npm run build
cd ..
```

## Start

```bash
py -m backend
```

The server listens on http://127.0.0.1:5000 and serves:

- `/api/*` — JSON API
- `/` — built Vue frontend from `frontend/dist/`

SQLite database file is created automatically at `data/quiz_bank.db` on first start.

## Tests

```bash
py -m pytest tests -v
cd frontend && npm test
```
