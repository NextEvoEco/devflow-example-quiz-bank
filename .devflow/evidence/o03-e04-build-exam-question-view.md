# Evidence: Build In-Exam Question View and Submit Flow

**ID:** o03-e04-build-exam-question-view
**Task Ref:** `.devflow/tasks/o03/t04-build-exam-question-view.md`
**Executed By:** Cursor
**Execution Date:** 2026-07-09
**Execution Time:** ~14:09 UTC+8
**Status:** completed

---

## 1. Summary

Replaced the exam-taking placeholder with a full in-exam experience: attempt creation on start, one question at a time with selectable options, immediate answer persistence via API, free navigation via Previous/Next and question jump buttons, and Submit that stores the response payload and transitions to a results placeholder for t05.

---

## 2. Files Changed

| File                             | Change Type | Description                                                    |
| -------------------------------- | ----------- | -------------------------------------------------------------- |
| `frontend/index.html`            | modified    | Exam-taking UI and results placeholder page                    |
| `frontend/js/questions.js`       | modified    | `ExamTakingPage`, `ExamResultsPlaceholderPage`, router updates |
| `frontend/js/api.js`             | modified    | Exam API client helpers                                        |
| `frontend/css/styles.css`        | modified    | Exam-taking layout and option button styles                    |
| `tests/test_exam_taking_page.py` | created     | Markup, assets, and API flow tests                             |
| `tests/test_exam_list_page.py`   | modified    | Updated asset assertion for `ExamTakingPage`                   |

---

## 3. Behavior Added

* Start Exam creates attempt via `POST /api/exams/attempts`
* One question displayed with A–D option buttons; selected option highlighted
* Answer saved immediately via `PUT /api/exams/attempts/{id}/answers/{question_id}`
* Previous/Next navigation and numbered jump buttons restore prior selections
* Progress bar and "Question N of M" counter
* Submit on last question calls submit API and navigates to `#exam-results-{quizId}`
* Exit returns to exams list without submitting (attempt abandoned in DB)
* Submit response stored in `sessionStorage` for results page (t05)

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                | Result | Notes                                  |
| ---------------------------------------- | ------ | -------------------------------------- |
| Attempt created and first question loads | PASS   |                                        |
| Options highlighted on select            | PASS   | CSS `exam-option--selected`            |
| Save-answer API called on select         | PASS   | `saveExamAnswer` helper                |
| Navigation restores answers              | PASS   | sessionStorage + re-render             |
| Progress indicator shown                 | PASS   | Counter + progress bar                 |
| Submit passes payload to results view    | PASS   | `examResultsPayload` in sessionStorage |
| Navigating away before submit is safe    | PASS   | Exit link only                         |

### Test Output

```
89 passed in 1.81s
```

---

## 5. Known Limitations

* Results page is a placeholder until t05.
* Each exam load creates a new attempt (abandoned if user exits without submit).

---

## 6. Next Suggested Task

**Next task:** `o03/t05-build-results-page`
**Context:** Read `examResultsPayload` from sessionStorage and render full score summary and answer review.
