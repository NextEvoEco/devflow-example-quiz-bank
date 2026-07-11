// Quiz List page (o02/t03).
// Browses saved quizzes and routes to the Quiz Builder (create/edit, o02/t04)
// and delete confirmation. Kept separate from Question Bank logic.

(() => {
    const QUIZ_API = "/api/quizzes";

    const q = {};
    let pendingDeleteQuizId = null;

    document.addEventListener("DOMContentLoaded", () => {
        q.grid = document.getElementById("quiz-grid");
        q.count = document.getElementById("quiz-count");
        q.emptyState = document.getElementById("quiz-empty-state");

        // Delete dialog
        q.deleteOverlay = document.getElementById("quiz-delete-overlay");
        q.deleteText = document.getElementById("quiz-delete-text");

        document.getElementById("new-quiz-btn").addEventListener("click", () => openBuilder(null));
        document.getElementById("quiz-empty-new-btn").addEventListener("click", () => openBuilder(null));

        document.getElementById("quiz-delete-cancel").addEventListener("click", closeQuizDelete);
        document.getElementById("quiz-delete-confirm").addEventListener("click", confirmQuizDelete);
        q.deleteOverlay.addEventListener("click", (e) => {
            if (e.target === q.deleteOverlay) closeQuizDelete();
        });
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape") closeQuizDelete();
        });

        // Register the quiz list loader. The quizCreate page is owned by
        // quiz-builder.js (o02/t04).
        registerPage("quizList", loadQuizzes);
    });

    // --- Quiz list -----------------------------------------------------------

    async function loadQuizzes() {
        try {
            const response = await fetch(QUIZ_API);
            if (!response.ok) throw new Error(`Request failed: ${response.status}`);
            renderQuizzes(await response.json());
        } catch (err) {
            console.error("Failed to load quizzes", err);
            renderQuizzes([]);
        }
    }

    function renderQuizzes(quizzes) {
        q.count.textContent = String(quizzes.length);
        q.grid.innerHTML = "";

        if (quizzes.length === 0) {
            q.grid.hidden = true;
            q.emptyState.hidden = false;
            return;
        }

        q.emptyState.hidden = true;
        q.grid.hidden = false;
        for (const quiz of quizzes) {
            q.grid.appendChild(buildQuizCard(quiz));
        }
    }

    function buildQuizCard(quiz) {
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

        const actions = document.createElement("div");
        actions.className = "quiz-card-actions";

        const editBtn = document.createElement("button");
        editBtn.type = "button";
        editBtn.className = "btn btn-secondary";
        editBtn.textContent = "Edit";
        editBtn.addEventListener("click", () => openBuilder(quiz.id));

        const delBtn = document.createElement("button");
        delBtn.type = "button";
        delBtn.className = "btn btn-danger";
        delBtn.textContent = "Delete";
        delBtn.addEventListener("click", () => openQuizDelete(quiz));

        actions.appendChild(editBtn);
        actions.appendChild(delBtn);

        card.appendChild(top);
        card.appendChild(actions);
        return card;
    }

    // --- Navigation to the builder (quiz-builder.js owns the quizCreate page) -

    function openBuilder(quizId) {
        navigate("quizCreate", { quizId });
    }

    // --- Delete flow ---------------------------------------------------------

    function openQuizDelete(quiz) {
        pendingDeleteQuizId = quiz.id;
        q.deleteText.textContent =
            `"${quiz.name}" will be permanently removed. This action cannot be undone.`;
        q.deleteOverlay.hidden = false;
    }

    function closeQuizDelete() {
        q.deleteOverlay.hidden = true;
        pendingDeleteQuizId = null;
    }

    async function confirmQuizDelete() {
        if (pendingDeleteQuizId === null) return;
        const id = pendingDeleteQuizId;
        try {
            const response = await fetch(`${QUIZ_API}/${id}`, { method: "DELETE" });
            if (!response.ok && response.status !== 404) {
                throw new Error(`Delete failed: ${response.status}`);
            }
        } catch (err) {
            console.error("Delete failed", err);
        } finally {
            closeQuizDelete();
            await loadQuizzes();
        }
    }
})();
