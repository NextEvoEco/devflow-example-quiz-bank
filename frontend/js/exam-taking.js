// In-exam question view + submit flow (o03/t04).
// Owns the examTaking page: creates an attempt, shows one question at a time
// with free navigation (Prev/Next + question-number jumps), saves each answer
// immediately, and submits for scoring. Correct answers are never displayed.

(() => {
    const EXAM_API = "/api/exams";
    const QUIZ_API = "/api/quizzes";
    const LETTERS = ["A", "B", "C", "D"];

    const t = {};
    const state = {
        attemptId: null,
        quizId: null,
        quizName: "",
        questions: [], // ordered quiz questions (never render `correct`)
        answers: {},   // { [questionId]: "A" | "B" | "C" | "D" }
        index: 0,
    };

    document.addEventListener("DOMContentLoaded", () => {
        t.quizName = document.getElementById("exam-quiz-name");
        t.progressLabel = document.getElementById("exam-progress-label");
        t.progressFill = document.getElementById("exam-progress-fill");
        t.navNumbers = document.getElementById("exam-nav-numbers");
        t.questionText = document.getElementById("exam-question-text");
        t.options = document.getElementById("exam-options");
        t.prevBtn = document.getElementById("exam-prev-btn");
        t.nextBtn = document.getElementById("exam-next-btn");

        t.prevBtn.addEventListener("click", goPrev);
        t.nextBtn.addEventListener("click", goNext);
        document.getElementById("exam-exit-btn").addEventListener("click", () => navigate("examList"));

        registerPage("examTaking", startExam);
        // The examResults page is owned by exam-results.js (o03/t05).
    });

    // --- Start / load ---------------------------------------------------------

    async function startExam(opts = {}) {
        const quizId = opts.quizId ?? window.currentExamQuizId ?? null;
        if (quizId === null) return;

        try {
            const created = await postJSON(`${EXAM_API}/attempts`, { quiz_id: quizId });
            const quiz = await (await fetch(`${QUIZ_API}/${quizId}`)).json();

            state.attemptId = created.attempt_id;
            state.quizId = quizId;
            state.quizName = quiz.name;
            state.questions = quiz.questions;
            state.answers = {};
            state.index = 0;
        } catch (err) {
            console.error("Failed to start exam", err);
            return;
        }
        renderNumbers();
        render();
    }

    // --- Rendering ------------------------------------------------------------

    function render() {
        const total = state.questions.length;
        const question = state.questions[state.index];

        t.quizName.textContent = state.quizName;
        t.progressLabel.textContent = `Question ${state.index + 1} of ${total}`;
        t.progressFill.style.width = `${((state.index + 1) / total) * 100}%`;

        t.questionText.textContent = question.question;
        renderOptions(question);
        updateNumbers();

        // Previous dimmed on the first question.
        t.prevBtn.classList.toggle("is-dimmed", state.index === 0);
        // Next becomes Submit on the last question.
        const isLast = state.index === total - 1;
        t.nextBtn.textContent = isLast ? "Submit" : "Next";
    }

    function renderOptions(question) {
        t.options.innerHTML = "";
        const selected = state.answers[question.id];

        for (const letter of LETTERS) {
            const btn = document.createElement("button");
            btn.type = "button";
            btn.className = "exam-option";
            btn.dataset.option = letter;
            if (selected === letter) btn.classList.add("is-selected");

            const label = document.createElement("span");
            label.className = "exam-option-label";
            label.textContent = letter;

            const text = document.createElement("span");
            text.className = "exam-option-text";
            text.textContent = question[letter.toLowerCase()];

            btn.appendChild(label);
            btn.appendChild(text);

            if (selected === letter) {
                const check = document.createElement("span");
                check.className = "exam-option-check";
                check.textContent = "✓";
                btn.appendChild(check);
            }

            btn.addEventListener("click", () => selectOption(letter));
            t.options.appendChild(btn);
        }
    }

    function renderNumbers() {
        t.navNumbers.innerHTML = "";
        state.questions.forEach((_, i) => {
            const btn = document.createElement("button");
            btn.type = "button";
            btn.className = "exam-number";
            btn.textContent = String(i + 1);
            btn.addEventListener("click", () => jumpTo(i));
            t.navNumbers.appendChild(btn);
        });
    }

    function updateNumbers() {
        [...t.navNumbers.children].forEach((btn, i) => {
            const qid = state.questions[i].id;
            btn.classList.toggle("is-current", i === state.index);
            btn.classList.toggle("is-answered", state.answers[qid] !== undefined);
        });
    }

    // --- Interaction ----------------------------------------------------------

    async function selectOption(letter) {
        const question = state.questions[state.index];
        state.answers[question.id] = letter;
        renderOptions(question);
        updateNumbers();
        try {
            await putJSON(
                `${EXAM_API}/attempts/${state.attemptId}/answers/${question.id}`,
                { selected_option: letter }
            );
        } catch (err) {
            console.error("Failed to save answer", err);
        }
    }

    function goPrev() {
        if (state.index > 0) {
            state.index -= 1;
            render();
        }
    }

    function goNext() {
        if (state.index === state.questions.length - 1) {
            submitExam();
        } else {
            state.index += 1;
            render();
        }
    }

    function jumpTo(index) {
        state.index = index;
        render();
    }

    async function submitExam() {
        try {
            const result = await postJSON(`${EXAM_API}/attempts/${state.attemptId}/submit`, {});
            // Hand the payload to the results view (o03/t05).
            window.examResult = result;
            window.examResultQuiz = { id: state.quizId, name: state.quizName };
            navigate("examResults");
        } catch (err) {
            console.error("Failed to submit exam", err);
        }
    }

    // --- fetch helpers --------------------------------------------------------

    async function postJSON(url, body) {
        const resp = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });
        if (!resp.ok) throw new Error(`POST ${url} -> ${resp.status}`);
        return resp.status === 204 ? null : resp.json();
    }

    async function putJSON(url, body) {
        const resp = await fetch(url, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });
        if (!resp.ok) throw new Error(`PUT ${url} -> ${resp.status}`);
    }
})();
