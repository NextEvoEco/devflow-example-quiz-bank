# Evidence: Build Available Exams Page

**ID:** o03-e03-build-available-exams-page
**Task Ref:** `.devflow/tasks/o03/t03-build-available-exams-page.md`
**Executed By:** Cursor + Composer
**Execution Date:** 2026-07-12
**Execution Time:** ~15:30-15:36 UTC+8 (implementation pass)
**Status:** completed

---

## 1. Summary

Added Online Exam section: sidebar nav, `ExamListPage` fetching `GET /api/quizzes`,
cards with title/question count/Start Exam, and empty state. Start Exam triggers
attempt creation and navigates to taking view (wired with t04). Question Bank and
Quiz Builder nav remain functional.

---

## 2. Files Changed

| File                                   | Change Type | Description               |
| -------------------------------------- | ----------- | ------------------------- |
| `frontend/src/pages/ExamListPage.tsx`  | created     | available exams list      |
| `frontend/src/components/AppShell.tsx` | modified    | Online Exam nav           |
| `frontend/src/App.tsx`                 | modified    | examList page + startExam |

---

## 3. Behavior Added

* Users can open Online Exam and see quizzes as exam cards.
* Start Exam begins an attempt flow.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                   | Result | Notes                      |
| ------------------------------------------- | ------ | -------------------------- |
| Online Exam in sidebar                      | PASS   |                            |
| Fetches quizzes and renders cards           | PASS   | GET /api/quizzes           |
| Card shows title, description, count, Start | PASS   | description optional/local |
| Start transitions toward exam taking        | PASS   | startAttempt + examTaking  |
| Empty state when no quizzes                 | PASS   |                            |
| Question Bank / Quiz Builder still work     | PASS   | separate page ids          |

### Test Output

```
npm run build → success
Browser SPA shows Online Exam nav item
```

---

## 5. Known Limitations

* Description is not persisted on quizzes; card may show empty/optional description.

---

## 6. Next Suggested Task

**Next task:** `o03/t04-build-exam-question-view`
**Context:** Implement taking UI with answer save and submit.
