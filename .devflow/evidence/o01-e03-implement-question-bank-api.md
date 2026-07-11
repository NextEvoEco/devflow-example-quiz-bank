# Evidence: Implement Question Bank API

**ID:** o01-e03-implement-question-bank-api
**Task Ref:** `.devflow/tasks/o01/t03-implement-question-bank-api.md`
**Executed By:** Cursor
**Execution Date:** 2026-07-08
**Execution Time:** ~23:50-00:05 UTC+8
**Status:** partial

---

## 1. Summary

Implemented Question Bank HTTP endpoints under `/api/questions`, registered the blueprint with the Flask app, and added API integration tests for list, search, create, update, delete, and core error paths.

The code changes are in place, but task verification is currently blocked because the shell execution environment is not returning any output or exit status, including for trivial commands. As a result, the new API tests could not be executed in this session.

---

## 2. Files Changed

| File                          | Change Type | Description                                       |
| ----------------------------- | ----------- | ------------------------------------------------- |
| `backend/routes/__init__.py`  | created     | Routes package marker                             |
| `backend/routes/questions.py` | created     | Question Bank API blueprint                       |
| `backend/app.py`              | modified    | Registered the questions blueprint                |
| `tests/test_questions_api.py` | created     | API integration tests for success and error paths |
| `.devflow/status.md`          | modified    | Runtime state updated for o01/t03                 |

---

## 3. Behavior Added

* `GET /api/questions` returns all questions.
* `GET /api/questions?q=<term>` returns filtered questions by case-insensitive text search.
* `GET /api/questions/<id>` returns a single question or `404`.
* `POST /api/questions` creates a question and returns `201`.
* `PUT /api/questions/<id>` updates a question and returns `404` for missing records.
* `DELETE /api/questions/<id>` deletes a question and returns `204`.
* Validation errors return explicit `400` JSON responses with `error` and `errors`.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                                      | Result  | Notes                                                                 |
| ---------------------------------------------------------------------------------------------- | ------- | --------------------------------------------------------------------- |
| The app exposes endpoints that support question list, search, create, update, and delete flows | PARTIAL | Implemented in code; not runtime-verified in this session             |
| Invalid inputs and missing-question cases return basic explicit error responses                | PARTIAL | Implemented in code; not runtime-verified in this session             |
| Automated tests cover the main API success and failure paths for V1                            | PASS    | Tests were added for list/search/create/update/delete and error cases |

### Test Output

```text
Unable to capture pytest output in this session.

Attempted:
- py -m pytest -v
- python -m pytest -v
- cmd /c wrappers
- trivial echo command

Observed issue:
- shell runner returned no stdout/stderr and no exit status for all commands
```

---

## 5. Known Limitations

* Verification is blocked by the current shell execution issue, not by a code failure that was observed.
* Frontend Question Bank UI is still pending in `o01/t04`.
* No authentication, pagination, or quiz/exam endpoints were added.

---

## 6. Next Suggested Task

**Next task:** `o01/t04-build-question-bank-list-page` after first re-running `o01/t03` tests in a healthy shell.
**Context:** The API layer is implemented and the frontend can now target `/api/questions`, but the current session could not verify runtime behavior because command execution produced no output.
