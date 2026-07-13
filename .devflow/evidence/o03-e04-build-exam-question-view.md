# Evidence: Build Exam Question View

**ID:** o03-e04-build-exam-question-view
**Task Ref:** `.devflow/tasks/o03/t04-build-exam-question-view.md`
**Executed By:** Cursor + Composer
**Execution Date:** 2026-07-12
**Execution Time:** ~15:30-15:36 UTC+8 (implementation pass)
**Status:** completed

---

## 1. Summary

Implemented `ExamTakingPage`: loads quiz questions for an attempt, shows one question
at a time with A–D options, saves answers immediately via PUT, supports prev/next with
restored selections, progress indicator, submit → results, and exit without submit.

---

## 2. Files Changed

| File                                    | Change Type | Description                  |
| --------------------------------------- | ----------- | ---------------------------- |
| `frontend/src/pages/ExamTakingPage.tsx` | created     | in-exam UI                   |
| `frontend/src/api/exams.ts`             | created     | attempt/answer/submit client |
| `frontend/src/App.tsx`                  | modified    | examTaking wiring            |

---

## 3. Behavior Added

* Start exam creates attempt and shows first question.
* Selecting an option persists to the API immediately.
* Free navigation between questions; submit ends the exam.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                      | Result | Notes                         |
| ---------------------------------------------- | ------ | ----------------------------- |
| Start creates attempt and loads first question | PASS   | startAttempt + ExamTakingPage |
| Options labeled; selected highlighted          | PASS   |                               |
| Select calls save-answer API                   | PASS   | PUT answers                   |
| Prev/Next restore selections                   | PASS   | local answer map              |
| Progress indicator                             | PASS   | e.g. n / total                |
| Submit calls API and goes to results           | PASS   |                               |
| Exit before submit does not crash              | PASS   | navigate examList             |

### Test Output

```
npm run build → success
HTTP smoke: PUT answers 204; POST submit 200
```

---

## 5. Known Limitations

* Abandoned attempts remain in DB unscored (by design).

---

## 6. Next Suggested Task

**Next task:** `o03/t05-build-results-page`
**Context:** Render submit payload review + retry/back actions.
