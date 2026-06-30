# Evidence: Build In-Exam Question View and Submit Flow

**ID:** o03-e04-build-exam-question-view
**Task Ref:** `.devflow/tasks/o03/t04-build-exam-question-view.md`
**Executed By:** Cursor
**Execution Date:** 2026-06-30
**Execution Time:** ~1 hr
**Status:** completed

---

## 1. Summary

Implemented the full in-exam experience: creating an attempt on start, one-question-at-a-time UI with option buttons, immediate answer saves via API, question jump navigation, and submit flow that stores the response and navigates to a results placeholder. Leaving Online Exam before submit abandons the in-memory session without errors.

---

## 2. Files Changed

| File                             | Change Type | Description                                       |
| -------------------------------- | ----------- | ------------------------------------------------- |
| `frontend/index.html`            | modified    | In-exam UI shell and results placeholder          |
| `frontend/js/exam-taking.js`     | created     | Exam session, navigation, API calls, submit       |
| `frontend/js/exam-list.js`       | modified    | Expanded `examState`, removed placeholder handler |
| `frontend/js/navigation.js`      | modified    | `examResults` route and abandon-on-exit logic     |
| `frontend/css/app.css`           | modified    | Exam taking and results styles                    |
| `tests/test_exam_taking_page.py` | created     | Shell, assets, and API flow tests                 |
| `tests/test_exam_list_page.py`   | modified    | Updated state assertion                           |

---

## 3. Behavior Added

* `POST /api/exams/attempts` on exam start; `attempt_id` stored in `examState`
* One question view with A–D option buttons and selected-state styling
* `PUT` save-answer on each selection
* Previous / Next navigation plus numbered jump buttons
* Submit on last question calls submit API and navigates to `#examResults`
* `examState.submitResult` holds payload for t05 results page
* Exit or sidebar navigation away abandons in-memory session

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                      | Result | Notes                              |
| ---------------------------------------------- | ------ | ---------------------------------- |
| Start creates attempt and loads first question | PASS   | `initializeExamSession`            |
| Options highlighted when selected              | PASS   | `is-selected` class                |
| Save-answer API on select                      | PASS   | `saveExamAnswer`                   |
| Prev/Next restores answers                     | PASS   | `examAnswers` keyed by question id |
| Progress indicator                             | PASS   | `Question N of M` + progress bar   |
| Submit passes payload to results view          | PASS   | `submitResult` + `#examResults`    |
| Navigate away without crash                    | PASS   | `abandonExamSession` in navigation |

### Test Output

```
90 passed in full suite
```

---

## 5. Known Limitations

* Results page is a placeholder only (t05).
* Submit button appears as Next/Submit toggle on last question per UI spec.

---

## 6. Next Suggested Task

**Next task:** `o03/t05-build-results-page`
**Context:** Use `window.examState.submitResult` from submit response to render score summary and answer review.
