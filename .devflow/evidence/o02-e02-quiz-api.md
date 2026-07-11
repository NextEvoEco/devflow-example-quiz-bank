# Evidence: Quiz CRUD API

**ID:** o02-e02-quiz-api
**Task Ref:** `.devflow/tasks/o02/t02-quiz-api.md`
**Executed By:** Claude Code
**Execution Date:** 2026-07-07
**Execution Time:** ~50 min
**Status:** completed

---

## 1. Summary

Implemented the Quiz management backend on top of the schema v2 join table,
following the V1 Question Bank pattern (repository + Flask blueprint + repo on
`app.config`). Added `QuizRepository` and a `/api/quizzes` blueprint covering
list, get, create, update, delete. Quizzes store only ordered question
references (position = request array index). Validation rejects saving with a
descriptive `400` when: fewer than 3 questions, a duplicate question id, a
non-existent question id, or a blank name. `GET /api/quizzes/<id>` returns full
ordered question objects (for the t05 preview, no extra call). The Question Bank
routes and repository were not modified. Verified with 76 passing tests (16 new)
plus a live `curl` session against the running server.

---

## 2. Files Changed

| File                         | Change Type | Description                                                                                                                              |
| ---------------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `backend/quiz_validation.py` | created     | `validate_quiz`: name required, list shape, min-3, no duplicates (structural)                                                            |
| `backend/quiz_repository.py` | created     | `QuizRepository`: list (with counts), get (ordered question objects), create/update/delete; question-existence check; ordered-row insert |
| `backend/routes/quizzes.py`  | created     | `/api/quizzes` blueprint (list/get/create/update/delete, error mapping)                                                                  |
| `backend/routes/__init__.py` | modified    | export `quizzes_bp`                                                                                                                      |
| `backend/app.py`             | modified    | build `QuizRepository`, store on `app.config`, register `quizzes_bp` (QB wiring untouched)                                               |
| `tests/test_quizzes_api.py`  | created     | 16 tests: create/validate/list/get/update/delete + QB-unaffected + cascade                                                               |
| `tests/test_v1_release.py`   | modified    | scope guard updated: `/api/quizzes` is now in-scope (V2); Online Exam stays absent                                                       |

---

## 3. Behavior Added

* `GET /api/quizzes` — list quizzes with `id`, `name`, `created_at`, `question_count`.
* `POST /api/quizzes` — create from `{name, questionIds}`; `201` with the created quiz (ordered `questionIds` + full `questions`).
* `GET /api/quizzes/<id>` — quiz detail including ordered full question objects; `404` if absent.
* `PUT /api/quizzes/<id>` — update name and/or question list (replaces the ordered set); `400`/`404` as appropriate.
* `DELETE /api/quizzes/<id>` — `204`; join rows removed by cascade; `404` if absent.
* Validation (`400` with `fields`): min 3 questions, no duplicate ids, all ids must exist, name required.
* Because the join FK cascades, deleting a question through the **unchanged** Question Bank API automatically drops it from any quiz's list.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                              | Result | Notes                                                    |
| ---------------------------------------------------------------------- | ------ | -------------------------------------------------------- |
| `POST /api/quizzes` creates a quiz and returns 201                     | PASS   | test + curl (returns ordered questions)                  |
| `POST /api/quizzes` with fewer than 3 questions returns 400            | PASS   | "a quiz requires at least 3 questions"                   |
| `POST /api/quizzes` with a non-existent question ID returns 400        | PASS   | "question IDs do not exist: [99999]"                     |
| `GET /api/quizzes` returns a list of quizzes                           | PASS   | includes `question_count`                                |
| `GET /api/quizzes/<id>` returns details incl. ordered question objects | PASS   | full question fields, order preserved                    |
| `PUT /api/quizzes/<id>` updates name and/or question list              | PASS   | rename + replace ids verified                            |
| `DELETE /api/quizzes/<id>` removes the quiz and its references         | PASS   | 204 then 404; join rows cascade-deleted                  |
| All existing Question Bank API tests continue to pass                  | PASS   | full suite green; `test_question_bank_still_works` added |

### Test Output

```
$ python -m pytest -q
76 passed in 1.75s
# (a transient PytestCacheWarning appeared once due to a Windows .pytest_cache
#  file-lock race during cleanup; unrelated to the code, does not affect results.)

# Live curl against py -m backend:
POST /api/quizzes {name, ids:[3,1,2]}      -> 201, questionIds [3,1,2], full ordered questions
POST /api/quizzes {2 ids}                   -> 400 "a quiz requires at least 3 questions"
POST /api/quizzes {ids incl 99999}          -> 400 "question IDs do not exist: [99999]"
GET  /api/quizzes                           -> 200 [{... question_count: 3}]
PUT  /api/quizzes/1 {name:Renamed, ids}     -> 200, name+ids updated
DELETE /api/questions/2 (referenced)        -> 204; quiz then lists [1,4] (cascade)
DELETE /api/quizzes/1                        -> 204; GET -> 404
GET  /api/exams                             -> 404 (still out of scope)
```

---

## 5. Known Limitations

* No frontend yet — quiz list/builder/preview pages are `o02/t03`–`t05`.
* `quizzes.description` is not stored (out of scope per the objective; see o02-e01).
* Reorder is expressed purely by array order in `questionIds`; there is no
  separate reorder endpoint (the builder in t04 will send the full ordered list).

---

## 6. Next Suggested Task

**Next task:** `o02/t03-quiz-list-page`
**Context:** The API is ready for the frontend. `GET /api/quizzes` gives
`{id, name, created_at, question_count}` for the list/cards; `GET /api/quizzes/<id>`
returns `{name, questionIds, questions:[...]}` for edit/preview. The sidebar
already has an (inactive) Quiz Builder nav item and the frontend uses a single
`currentPage` model per `ui-spec.md` (`quizList`, `quizCreate`). t03 should
activate the Quiz Builder nav, render the quiz card grid + empty state, and wire
New/Edit/Delete navigation (create/edit form is t04, preview is t05). Validation
errors surface as `{"error", "fields": {...}}`, consistent with the QB editor.
