// Quiz Builder page (o02/t04) — create / edit a quiz.
// Owns the `quizCreate` page: name input, question browser, selected panel with
// manual reorder, min-3 validation, and save (POST/PUT). Preview is o02/t05.

(() => {
    const QUIZ_API = "/api/quizzes";
    const QUESTION_API = "/api/questions";
    const MIN_QUESTIONS = 3;

    const b = {};
    let editingQuizId = null;      // null = create mode
    let allQuestions = [];         // full question bank
    let selected = [];             // ordered array of selected question objects
    let availableSearch = "";

    document.addEventListener("DOMContentLoaded", () => {
        b.title = document.getElementById("quiz-builder-title");
        b.formError = document.getElementById("quiz-form-error");
        b.name = document.getElementById("quiz-name");
        b.selectedList = document.getElementById("selected-list");
        b.selectedEmpty = document.getElementById("selected-empty");
        b.selectedCount = document.getElementById("selected-count");
        b.availableList = document.getElementById("available-list");
        b.availableEmpty = document.getElementById("available-empty");
        b.availableSearch = document.getElementById("available-search");

        b.availableSearch.addEventListener("input", (e) => {
            availableSearch = e.target.value;
            renderAvailable();
        });
        document.getElementById("quiz-back-link").addEventListener("click", () => navigate("quizList"));
        document.getElementById("quiz-cancel-btn").addEventListener("click", () => navigate("quizList"));
        document.getElementById("quiz-save-btn").addEventListener("click", saveQuiz);
        document.getElementById("quiz-preview-btn").addEventListener("click", previewQuiz);

        registerPage("quizCreate", loadBuilder);
    });

    // --- Load / init ---------------------------------------------------------

    async function loadBuilder(opts = {}) {
        editingQuizId = opts.quizId ?? null;
        selected = [];
        availableSearch = "";
        b.availableSearch.value = "";
        clearError();

        try {
            allQuestions = await (await fetch(QUESTION_API)).json();
        } catch (err) {
            console.error("Failed to load questions", err);
            allQuestions = [];
        }

        if (editingQuizId === null) {
            b.title.textContent = "New Quiz";
            b.name.value = "";
        } else {
            b.title.textContent = "Edit Quiz";
            try {
                const quiz = await (await fetch(`${QUIZ_API}/${editingQuizId}`)).json();
                b.name.value = quiz.name;
                selected = quiz.questions.slice(); // already ordered by position
            } catch (err) {
                console.error("Failed to load quiz", err);
                b.name.value = "";
            }
        }

        render();
    }

    // --- Rendering -----------------------------------------------------------

    function render() {
        renderSelected();
        renderAvailable();
    }

    function renderSelected() {
        b.selectedCount.textContent = String(selected.length);
        b.selectedList.innerHTML = "";

        if (selected.length === 0) {
            b.selectedEmpty.hidden = false;
            return;
        }
        b.selectedEmpty.hidden = true;

        selected.forEach((question, index) => {
            b.selectedList.appendChild(buildSelectedRow(question, index));
        });
    }

    function buildSelectedRow(question, index) {
        const row = document.createElement("div");
        row.className = "builder-row";
        row.dataset.id = question.id;

        row.appendChild(buildRowText(question));

        const controls = document.createElement("div");
        controls.className = "builder-row-controls";

        const up = document.createElement("button");
        up.type = "button";
        up.className = "reorder-btn";
        up.textContent = "↑";
        up.setAttribute("aria-label", "Move up");
        up.disabled = index === 0;
        up.addEventListener("click", () => moveSelected(index, -1));

        const down = document.createElement("button");
        down.type = "button";
        down.className = "reorder-btn";
        down.textContent = "↓";
        down.setAttribute("aria-label", "Move down");
        down.disabled = index === selected.length - 1;
        down.addEventListener("click", () => moveSelected(index, 1));

        const remove = document.createElement("button");
        remove.type = "button";
        remove.className = "remove-btn";
        remove.textContent = "×";
        remove.setAttribute("aria-label", "Remove");
        remove.addEventListener("click", () => removeSelected(question.id));

        controls.appendChild(up);
        controls.appendChild(down);
        controls.appendChild(remove);
        row.appendChild(controls);
        return row;
    }

    function renderAvailable() {
        const selectedIds = new Set(selected.map((q) => q.id));
        const term = availableSearch.trim().toLowerCase();

        const available = allQuestions.filter((q) => {
            if (selectedIds.has(q.id)) return false;
            if (term && !q.question.toLowerCase().includes(term)) return false;
            return true;
        });

        b.availableList.innerHTML = "";
        if (available.length === 0) {
            b.availableEmpty.hidden = false;
            return;
        }
        b.availableEmpty.hidden = true;

        for (const question of available) {
            b.availableList.appendChild(buildAvailableRow(question));
        }
    }

    function buildAvailableRow(question) {
        const row = document.createElement("div");
        row.className = "builder-row";
        row.dataset.id = question.id;

        row.appendChild(buildRowText(question));

        const addBtn = document.createElement("button");
        addBtn.type = "button";
        addBtn.className = "btn btn-secondary btn-add";
        addBtn.textContent = "Add";
        addBtn.addEventListener("click", () => addSelected(question.id));

        row.appendChild(addBtn);
        return row;
    }

    function buildRowText(question) {
        const wrap = document.createElement("div");
        wrap.className = "builder-row-text";

        const text = document.createElement("span");
        text.className = "builder-row-question";
        text.textContent = question.question;

        const badge = document.createElement("span");
        const level = (question.difficulty || "Medium").toLowerCase();
        badge.className = `difficulty-badge difficulty-${level}`;
        badge.textContent = question.difficulty || "Medium";

        wrap.appendChild(text);
        wrap.appendChild(badge);
        return wrap;
    }

    // --- Mutations -----------------------------------------------------------

    function addSelected(questionId) {
        if (selected.some((q) => q.id === questionId)) return; // no duplicates
        const question = allQuestions.find((q) => q.id === questionId);
        if (!question) return;
        selected.push(question);
        render();
    }

    function removeSelected(questionId) {
        selected = selected.filter((q) => q.id !== questionId);
        render();
    }

    function moveSelected(index, delta) {
        const target = index + delta;
        if (target < 0 || target >= selected.length) return;
        [selected[index], selected[target]] = [selected[target], selected[index]];
        render();
    }

    // --- Save ----------------------------------------------------------------

    async function saveQuiz() {
        clearError();
        const name = b.name.value.trim();

        if (!name) {
            showError("Quiz name is required.");
            return;
        }
        if (selected.length < MIN_QUESTIONS) {
            showError(`A quiz requires at least ${MIN_QUESTIONS} questions.`);
            return;
        }

        const payload = { name, questionIds: selected.map((q) => q.id) };
        const isEdit = editingQuizId !== null;
        const url = isEdit ? `${QUIZ_API}/${editingQuizId}` : QUIZ_API;
        const method = isEdit ? "PUT" : "POST";

        try {
            const response = await fetch(url, {
                method,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });
            if (response.ok) {
                navigate("quizList");
                return;
            }
            const body = await response.json().catch(() => ({}));
            if (response.status === 400 && body.fields) {
                showError(Object.values(body.fields).join(" "));
            } else {
                showError(body.error || "Could not save the quiz. Please try again.");
            }
        } catch (err) {
            console.error("Save failed", err);
            showError("Network error. Please try again.");
        }
    }

    // --- Preview (implemented in o02/t05) ------------------------------------

    function previewQuiz() {
        const draft = { name: b.name.value.trim(), questions: selected.slice() };
        if (typeof window.openQuizPreview === "function") {
            window.openQuizPreview(draft);
        } else {
            console.info("Quiz preview is implemented in o02/t05.", draft);
        }
    }

    // --- Error helpers -------------------------------------------------------

    function showError(message) {
        b.formError.textContent = message;
        b.formError.hidden = false;
    }

    function clearError() {
        b.formError.hidden = true;
        b.formError.textContent = "";
    }
})();
