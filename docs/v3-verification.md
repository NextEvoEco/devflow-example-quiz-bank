# V3 Online Exam Verification

1. Start PostgreSQL, build the frontend with `npm run build`, then run
   `backend\mvnw spring-boot:run`.
2. Open `http://127.0.0.1:5000`, select **Online Exam**, and confirm saved quizzes
   appear as Available Exams.
3. Start an exam, choose an option, navigate back and forth, and confirm the selected
   option remains highlighted.
4. Submit with at least one correct and one incorrect answer. Confirm the score,
   percentage, and Answer Review match the choices.
5. Retry the quiz and return to Available Exams.
6. Run `backend\mvnw test`, `frontend\npm test`, and `frontend\npm run build`.
