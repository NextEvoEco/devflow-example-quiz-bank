# Evidence: Implement Question Bank API

**ID:** o01-e03-implement-question-bank-api
**Task Ref:** `.devflow/tasks/o01/t03-implement-question-bank-api.md`
**Executed By:** Cursor + Composer
**Execution Date:** 2026-07-12
**Execution Time:** 15:24-15:26 UTC+8, ~10 min
**Status:** completed

---

## 1. Summary

Exposed Question Bank HTTP endpoints on `/api/questions` (list/search, get, create,
update, delete). JSON uses shared field names (`option_a`..`option_d`, `correct`,
`difficulty`). Validation failures return 400 with `error`/`errors`; missing IDs
return 404. Covered by MockMvc API tests.

---

## 2. Files Changed

| File                                                              | Change Type | Description                                       |
| ----------------------------------------------------------------- | ----------- | ------------------------------------------------- |
| `backend/src/main/java/com/quizbank/web/QuestionController.java`  | created     | REST endpoints                                    |
| `backend/src/main/java/com/quizbank/web/ApiExceptionHandler.java` | created     | 400/404 mapping                                   |
| `backend/src/main/java/com/quizbank/web/NotFoundException.java`   | created     | not-found type                                    |
| `backend/src/main/java/com/quizbank/question/Question.java`       | modified    | Jackson `@JsonProperty` for option_* / timestamps |
| `backend/src/test/java/com/quizbank/web/QuestionApiTest.java`     | created     | API success/failure tests                         |

---

## 3. Behavior Added

* `GET /api/questions` and `GET /api/questions?q=`
* `GET /api/questions/{id}`
* `POST /api/questions` → 201
* `PUT /api/questions/{id}`
* `DELETE /api/questions/{id}`
* Explicit validation and not-found error JSON

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                          | Result | Notes               |
| -------------------------------------------------- | ------ | ------------------- |
| Endpoints support list/search/create/update/delete | PASS   | QuestionApiTest     |
| Invalid/missing return explicit errors             | PASS   | 400 + 404 cases     |
| Automated API tests cover success and failure      | PASS   | `./mvnw test` green |

### Test Output

```
./mvnw test → BUILD SUCCESS (includes QuestionApiTest)
```

---

## 5. Known Limitations

* No frontend wiring yet (o01/t04–t05).

---

## 6. Next Suggested Task

**Next task:** `o01/t04-build-question-bank-list-page`
**Context:** Build React Question Bank list + search + empty state against `/api/questions`.
