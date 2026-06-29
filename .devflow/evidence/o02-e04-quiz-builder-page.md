# Evidence: Quiz Builder Page

**ID:** o02-e04-quiz-builder-page
**Task:** o02/t04-quiz-builder-page
**Objective:** o02-quiz-builder-v1
**Date:** 2026-06-28

---

## Summary

Implemented the Quiz Builder create/edit page with question selection, reordering, validation, save flows, and a preview entry point for t05.

---

## Changes

| Area | Details |
| ---- | ------- |
| `frontend/index.html` | Replaced builder stub with name input, selected/available panels, footer actions, and preview modal shell |
| `frontend/js/quiz-builder.js` | New module: load create/edit data, add/remove/reorder questions, save via API, preview hook |
| `frontend/js/navigation.js` | Wired `refreshQuizBuilder` on `#quizCreate` routes |
| `frontend/js/quiz-list.js` | Removed builder stub refresh helper |
| `frontend/css/app.css` | Builder layout, row actions, preview modal styles |
| `tests/test_quiz_builder_page.py` | Shell, asset, and API integration smoke tests |

---

## Verification

```text
py -m pytest tests/test_quiz_builder_page.py -q
py -m pytest -q
```

Manual checks:

- Navigate to `#quizCreate` — new quiz form loads all questions
- Add 3+ questions, reorder with Up/Down, save — returns to quiz list
- Edit existing quiz — name and order pre-populated from `GET /api/quizzes/<id>`
- Save with fewer than 3 questions — client error shown
- Preview button — opens modal with quiz name and ordered question text (full preview UI deferred to t05)

---

## Notes

- Preview modal is intentionally minimal; t05 will expand preview behavior.
- Question Bank module unchanged.
