// Exam Results page (o03/t05).
// Renders the just-submitted attempt from window.examResult (set by
// exam-taking.js). Makes no API calls — it only reads the payload already in
// state. Retry Quiz restarts the same quiz; Back to Exams returns to the list.

(() => {
    const r = {};

    document.addEventListener("DOMContentLoaded", () => {
        r.quizName = document.getElementById("results-quiz-name");
        r.pct = document.getElementById("results-pct");
        r.frac = document.getElementById("results-frac");
        r.ring = document.getElementById("results-ring");
        r.correct = document.getElementById("results-correct");
        r.incorrect = document.getElementById("results-incorrect");
        r.review = document.getElementById("results-review");

        document.getElementById("results-back-btn").addEventListener("click", () => navigate("examList"));
        document.getElementById("results-retry-btn").addEventListener("click", retryQuiz);

        registerPage("examResults", render);
    });

    function render() {
        const result = window.examResult;
        if (!result) return;

        const quiz = window.examResultQuiz || {};
        r.quizName.textContent = quiz.name || "";

        const correct = result.score;
        const incorrect = result.total - result.score;
        r.correct.textContent = String(correct);
        r.incorrect.textContent = String(incorrect);

        renderRing(result.percentage, result.score, result.total);
        renderReview(result.answers || []);
    }

    function renderRing(percentage, score, total) {
        r.pct.textContent = `${percentage}%`;
        r.frac.textContent = `${score} / ${total}`;

        const radius = Number(r.ring.getAttribute("r"));
        const circumference = 2 * Math.PI * radius;
        r.ring.style.strokeDasharray = String(circumference);
        r.ring.style.strokeDashoffset = String(circumference * (1 - percentage / 100));

        r.ring.classList.remove("ring-green", "ring-amber", "ring-red");
        const band = percentage >= 70 ? "ring-green" : percentage >= 50 ? "ring-amber" : "ring-red";
        r.ring.classList.add(band);
    }

    function renderReview(answers) {
        r.review.innerHTML = "";
        answers.forEach((answer) => {
            r.review.appendChild(buildReviewRow(answer));
        });
    }

    function buildReviewRow(answer) {
        const row = document.createElement("div");
        row.className = `review-row ${answer.is_correct ? "is-correct" : "is-incorrect"}`;

        const icon = document.createElement("div");
        icon.className = "review-icon";
        icon.textContent = answer.is_correct ? "✓" : "✗";

        const body = document.createElement("div");
        body.className = "review-body";

        const question = document.createElement("p");
        question.className = "review-question";
        question.textContent = answer.question_text;
        body.appendChild(question);

        const yours = document.createElement("p");
        yours.className = "review-answer";
        yours.textContent = `Your answer: ${formatOption(answer, answer.selected_option)}`;
        body.appendChild(yours);

        // Only show the correct answer when the user got it wrong.
        if (!answer.is_correct) {
            const correct = document.createElement("p");
            correct.className = "review-correct";
            correct.textContent = `Correct: ${formatOption(answer, answer.correct_option)}`;
            body.appendChild(correct);
        }

        const badge = document.createElement("span");
        badge.className = `review-badge ${answer.is_correct ? "badge-correct" : "badge-incorrect"}`;
        badge.textContent = answer.is_correct ? "Correct" : "Incorrect";

        row.appendChild(icon);
        row.appendChild(body);
        row.appendChild(badge);
        return row;
    }

    function formatOption(answer, letter) {
        if (!letter) return "Not answered";
        const text = answer.options ? answer.options[letter] : "";
        return text ? `${letter}: ${text}` : letter;
    }

    function retryQuiz() {
        const quizId = (window.examResultQuiz && window.examResultQuiz.id) || window.currentExamQuizId;
        if (quizId == null) {
            navigate("examList");
            return;
        }
        // exam-taking.js creates a fresh attempt for a new run of the same quiz.
        navigate("examTaking", { quizId });
    }
})();
