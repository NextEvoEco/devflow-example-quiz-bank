# 05 — API Reference

HTTP API exposed by the Spring Boot backend on port **5000**.

Base URL (local): `http://127.0.0.1:5000`

All request/response bodies are JSON unless noted. Field names use `snake_case`
where shown below.

Commands below use **bash** (`curl`).

---

## Conventions

### Success

| Situation  | Status |
| ---------- | ------ |
| OK         | `200`  |
| Created    | `201`  |
| No content | `204`  |

### Errors

| Situation                     | Status | Body shape                              |
| ----------------------------- | ------ | --------------------------------------- |
| Validation failure            | `400`  | `{ "error": "...", "errors": ["..."] }` |
| Not found                     | `404`  | `{ "error": "..." }`                    |
| Conflict (e.g. double submit) | `409`  | `{ "error": "..." }`                    |

---

## Health

### `GET /api/health`

Liveness / DB smoke check.

**Response `200`**

```json
{
  "status": "ok",
  "app": "quiz-bank",
  "schemaBootstrapRows": 1
}
```

```bash
curl -s http://127.0.0.1:5000/api/health
```

---

## Questions

Base path: `/api/questions`

### Question object

```json
{
  "id": 1,
  "question": "Which is the largest continent?",
  "option_a": "Asia",
  "option_b": "Africa",
  "option_c": "Europe",
  "option_d": "Oceania",
  "correct": "A",
  "difficulty": "Easy",
  "created_at": "2026-07-12T07:00:00Z",
  "updated_at": "2026-07-12T07:00:00Z"
}
```

| Field                   | Type   | Notes                                                          |
| ----------------------- | ------ | -------------------------------------------------------------- |
| `question`              | string | Required, non-blank                                            |
| `option_a` … `option_d` | string | Required, non-blank                                            |
| `correct`               | string | `A` \| `B` \| `C` \| `D`                                       |
| `difficulty`            | string | `Easy` \| `Medium` \| `Hard` (defaults to `Medium` if omitted) |

### `GET /api/questions`

List questions.

| Query | Description                                                 |
| ----- | ----------------------------------------------------------- |
| `q`   | Optional case-insensitive substring filter on question text |

**Response `200`:** array of question objects.

```bash
curl -s 'http://127.0.0.1:5000/api/questions'
curl -s 'http://127.0.0.1:5000/api/questions?q=continent'
```

### `GET /api/questions/{id}`

**Response `200`:** question object.  
**Response `404`:** question not found.

```bash
curl -s http://127.0.0.1:5000/api/questions/1
```

### `POST /api/questions`

Create a question.

**Request**

```json
{
  "question": "Capital of Japan?",
  "option_a": "Tokyo",
  "option_b": "Osaka",
  "option_c": "Kyoto",
  "option_d": "Nagoya",
  "correct": "A",
  "difficulty": "Medium"
}
```

**Response `201`:** created question (includes `id`).  
**Response `400`:** validation error.

```bash
curl -s -X POST http://127.0.0.1:5000/api/questions \
  -H 'Content-Type: application/json' \
  -d '{
    "question": "Capital of Japan?",
    "option_a": "Tokyo",
    "option_b": "Osaka",
    "option_c": "Kyoto",
    "option_d": "Nagoya",
    "correct": "A",
    "difficulty": "Medium"
  }'
```

### `PUT /api/questions/{id}`

Update a question (same body shape as create).

**Response `200`:** updated question.  
**Response `404`:** missing id.  
**Response `400`:** validation error.

```bash
curl -s -X PUT http://127.0.0.1:5000/api/questions/1 \
  -H 'Content-Type: application/json' \
  -d '{
    "question": "Capital of Japan?",
    "option_a": "Tokyo",
    "option_b": "Osaka",
    "option_c": "Kyoto",
    "option_d": "Nagoya",
    "correct": "A",
    "difficulty": "Easy"
  }'
```

### `DELETE /api/questions/{id}`

**Response `200`**

```json
{ "deleted": true, "id": 1 }
```

**Response `404`:** missing id.

```bash
curl -s -X DELETE http://127.0.0.1:5000/api/questions/1
```

---

## Quizzes

Base path: `/api/quizzes`

A quiz must include **at least 3** distinct existing question IDs. Order in
`question_ids` is stored as `position`.

### Summary object (list)

```json
{
  "id": 1,
  "name": "World Geography Starter 3",
  "question_count": 3,
  "created_at": "2026-07-12T07:00:00Z"
}
```

### Detail object (get / create / update)

```json
{
  "id": 1,
  "name": "World Geography Starter 3",
  "question_ids": [7, 8, 9],
  "questions": [ { "id": 7, "question": "...", "option_a": "...", "...": "..." } ],
  "question_count": 3,
  "created_at": "2026-07-12T07:00:00Z"
}
```

### `GET /api/quizzes`

**Response `200`:** array of summary objects.

```bash
curl -s http://127.0.0.1:5000/api/quizzes
```

### `GET /api/quizzes/{id}`

**Response `200`:** detail object with ordered full question payloads (for preview).  
**Response `404`:** quiz not found.

```bash
curl -s http://127.0.0.1:5000/api/quizzes/1
```

### `POST /api/quizzes`

**Request**

```json
{
  "name": "My Quiz",
  "question_ids": [1, 2, 3]
}
```

**Response `201`:** detail object.  
**Response `400`:** fewer than 3 questions, duplicates, missing name, or unknown question id.

```bash
curl -s -X POST http://127.0.0.1:5000/api/quizzes \
  -H 'Content-Type: application/json' \
  -d '{"name":"My Quiz","question_ids":[1,2,3]}'
```

### `PUT /api/quizzes/{id}`

Same body as create. Replaces name and the full ordered question list.

**Response `200`:** detail object.  
**Response `404`:** quiz not found.  
**Response `400`:** validation error.

```bash
curl -s -X PUT http://127.0.0.1:5000/api/quizzes/1 \
  -H 'Content-Type: application/json' \
  -d '{"name":"My Quiz Updated","question_ids":[1,2,3,4]}'
```

### `DELETE /api/quizzes/{id}`

**Response `200`**

```json
{ "deleted": true, "id": 1 }
```

**Response `404`:** quiz not found.

```bash
curl -s -X DELETE http://127.0.0.1:5000/api/quizzes/1
```

---

## Exams

Base path: `/api/exams`

Exam flow: create attempt → save answers → submit for scoring.

### `POST /api/exams/attempts`

Start an attempt for a quiz.

**Request**

```json
{ "quiz_id": 1 }
```

**Response `201`**

```json
{ "attempt_id": 42 }
```

**Response `404`:** quiz not found.

```bash
curl -s -X POST http://127.0.0.1:5000/api/exams/attempts \
  -H 'Content-Type: application/json' \
  -d '{"quiz_id":1}'
```

### `PUT /api/exams/attempts/{attempt_id}/answers/{question_id}`

Save or replace one answer. May be called repeatedly before submit.

**Request**

```json
{ "selected_option": "A" }
```

`selected_option` must be `A`, `B`, `C`, or `D` when provided.

**Response `204`:** saved.  
**Response `404`:** attempt or question not in this quiz.  
**Response `409`:** attempt already submitted.

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  -X PUT http://127.0.0.1:5000/api/exams/attempts/42/answers/7 \
  -H 'Content-Type: application/json' \
  -d '{"selected_option":"A"}'
# expect: 204
```

### `POST /api/exams/attempts/{attempt_id}/submit`

Score the attempt. Idempotent-safe: a second submit returns conflict.

**Response `200`**

```json
{
  "score": 2,
  "total": 3,
  "percentage": 67,
  "answers": [
    {
      "question_id": 7,
      "question_text": "Which is the largest continent?",
      "selected_option": "A",
      "correct_option": "A",
      "is_correct": true,
      "option_a": "Asia",
      "option_b": "Africa",
      "option_c": "Europe",
      "option_d": "Oceania"
    }
  ]
}
```

| Field                  | Meaning                                   |
| ---------------------- | ----------------------------------------- |
| `score`                | Number of correct answers                 |
| `total`                | Number of questions in the quiz           |
| `percentage`           | Rounded percent                           |
| `answers[].is_correct` | `selected_option` equals `correct_option` |

**Response `404`:** attempt not found.  
**Response `409`:** already submitted.

```bash
curl -s -X POST http://127.0.0.1:5000/api/exams/attempts/42/submit
```

Correct options are returned **only** in the submit response (not while the exam is in progress).

---

## Static UI

| Method | Path          | Description                       |
| ------ | ------------- | --------------------------------- |
| `GET`  | `/`           | SPA `index.html`                  |
| `GET`  | `/index.html` | Same                              |
| `GET`  | `/assets/*`   | Built JS/CSS from `frontend/dist` |

---

## Example end-to-end

```bash
BASE=http://127.0.0.1:5000

create_q() {
  curl -s -X POST "$BASE/api/questions" \
    -H 'Content-Type: application/json' \
    -d "{\"question\":\"$1\",\"option_a\":\"A1\",\"option_b\":\"B1\",\"option_c\":\"C1\",\"option_d\":\"D1\",\"correct\":\"A\",\"difficulty\":\"Easy\"}" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])"
}

ID1=$(create_q 'Q1')
ID2=$(create_q 'Q2')
ID3=$(create_q 'Q3')

QUIZ_ID=$(curl -s -X POST "$BASE/api/quizzes" \
  -H 'Content-Type: application/json' \
  -d "{\"name\":\"Demo\",\"question_ids\":[$ID1,$ID2,$ID3]}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

ATTEMPT_ID=$(curl -s -X POST "$BASE/api/exams/attempts" \
  -H 'Content-Type: application/json' \
  -d "{\"quiz_id\":$QUIZ_ID}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['attempt_id'])")

for QID in "$ID1" "$ID2" "$ID3"; do
  curl -s -o /dev/null -X PUT "$BASE/api/exams/attempts/$ATTEMPT_ID/answers/$QID" \
    -H 'Content-Type: application/json' \
    -d '{"selected_option":"A"}'
done

curl -s -X POST "$BASE/api/exams/attempts/$ATTEMPT_ID/submit"
echo
```

---

## Related docs

- [02-configuration.md](02-configuration.md)
- [03-deployment.md](03-deployment.md)
- [04-user-guide.md](04-user-guide.md)
