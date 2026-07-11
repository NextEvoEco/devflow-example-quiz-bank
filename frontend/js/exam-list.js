// Available Exams page (o03/t03).
// Lists saved quizzes as exam cards using the existing GET /api/quizzes.
// Start Exam stores the selected quiz id and routes to the exam-taking view
// (the question view itself is built in o03/t04). No exam API calls here.

(() => {
    const QUIZ_API = "/api/quizzes";

    const e = {};

    document.addEventListener("DOMContentLoaded", () => {
        e.grid = document.getElementById("exam-grid");
        e.emptyState = document.getElementById("exam-empty-state");

        // The examTaking page is owned by exam-taking.js (o03/t04).
        registerPage("examList", loadExams);
    });

    // --- Available Exams -----------------------------------------------------

    async function loadExams() {
        try {
            const response = await fetch(QUIZ_API);
            if (!response.ok) throw new Error(`Request failed: ${response.status}`);
            renderExams(await response.json());
        } catch (err) {
            console.error("Failed to load exams", err);
            renderExams([]);
        }
    }

    function renderExams(quizzes) {
        e.grid.innerHTML = "";
        if (quizzes.length === 0) {
            e.grid.hidden = true;
            e.emptyState.hidden = false;
            return;
        }
        e.emptyState.hidden = true;
        e.grid.hidden = false;
        for (const quiz of quizzes) {
            e.grid.appendChild(buildExamCard(quiz));
        }
    }

    function buildExamCard(quiz) {
        const card = document.createElement("div");
        card.className = "quiz-card";
        card.dataset.id = quiz.id;

        const top = document.createElement("div");
        top.className = "quiz-card-top";

        const name = document.createElement("h3");
        name.className = "quiz-card-name";
        name.textContent = quiz.name;

        const badge = document.createElement("span");
        badge.className = "count-badge";
        const n = quiz.question_count;
        badge.textContent = `${n} ${n === 1 ? "question" : "questions"}`;

        top.appendChild(name);
        top.appendChild(badge);

        const startBtn = document.createElement("button");
        startBtn.type = "button";
        startBtn.className = "btn btn-primary exam-start-btn";
        startBtn.textContent = "Start Exam";
        startBtn.addEventListener("click", () => startExam(quiz.id));

        card.appendChild(top);
        card.appendChild(startBtn);
        return card;
    }

    // --- Start Exam ----------------------------------------------------------

    function startExam(quizId) {
        // Carry the selected quiz into the exam-taking view (exam-taking.js).
        window.currentExamQuizId = quizId;
        navigate("examTaking", { quizId });
    }
})();
