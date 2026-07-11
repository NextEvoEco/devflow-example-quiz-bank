// Question Bank page (o01/t04 + o01/t05).
// List rendering + real-time search, plus add / edit / delete flows.

const API_BASE = "/api/questions";
const FIELD_NAMES = ["question", "a", "b", "c", "d", "correct", "difficulty"];

const els = {};
let currentSearch = "";
let editingId = null; // null = add mode, otherwise the id being edited
let pendingDeleteId = null;

document.addEventListener("DOMContentLoaded", () => {
    els.tbody = document.getElementById("question-tbody");
    els.table = document.getElementById("question-table");
    els.emptyState = document.getElementById("empty-state");
    els.emptyTitle = document.getElementById("empty-state-title");
    els.emptyText = document.getElementById("empty-state-text");
    els.count = document.getElementById("question-count");
    els.search = document.getElementById("search-input");

    // Editor modal
    els.editorOverlay = document.getElementById("editor-overlay");
    els.editorTitle = document.getElementById("editor-title");
    els.editorForm = document.getElementById("editor-form");
    els.formError = document.getElementById("form-error");

    // Delete dialog
    els.deleteOverlay = document.getElementById("delete-overlay");

    els.search.addEventListener("input", onSearchInput);
    document.getElementById("add-question-btn").addEventListener("click", openAdd);
    document.getElementById("empty-add-btn").addEventListener("click", openAdd);

    // Editor modal events
    document.getElementById("editor-close").addEventListener("click", closeEditor);
    document.getElementById("editor-cancel").addEventListener("click", closeEditor);
    els.editorForm.addEventListener("submit", onEditorSubmit);
    els.editorOverlay.addEventListener("click", (e) => {
        if (e.target === els.editorOverlay) closeEditor();
    });

    // Delete dialog events
    document.getElementById("delete-cancel").addEventListener("click", closeDelete);
    document.getElementById("delete-confirm").addEventListener("click", confirmDelete);
    els.deleteOverlay.addEventListener("click", (e) => {
        if (e.target === els.deleteOverlay) closeDelete();
    });

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            closeEditor();
            closeDelete();
        }
    });

    // The Question Bank page loads its own data when navigated to.
    registerPage("questions", loadQuestions);
    setupNavigation();
    navigate("questions");
});

// --- Navigation controller (shared across pages) ----------------------------
// Page modules register a loader; navigate() switches the visible page,
// updates the sidebar + top bar, and invokes the target page's loader.

window.pageLoaders = window.pageLoaders || {};

// Maps a page id to the sidebar nav item that should appear active for it.
const NAV_GROUP = {
    questions: "questions",
    quizList: "quizList",
    quizCreate: "quizList",
    examList: "examList",
    examTaking: "examList",
    examResults: "examList",
};
const TOP_BAR_TITLES = {
    questions: "Questions",
    quizList: "Quizzes",
    quizCreate: "Quiz Builder",
    examList: "Available Exams",
    examTaking: "Exam",
    examResults: "Results",
};

let currentPage = "questions";

function registerPage(page, loader) {
    window.pageLoaders[page] = loader;
}

function setupNavigation() {
    document.querySelectorAll(".sidebar-nav .nav-item[data-page]").forEach((btn) => {
        btn.addEventListener("click", () => navigate(btn.dataset.page));
    });
}

function navigate(page, opts = {}) {
    currentPage = page;

    document.querySelectorAll(".page").forEach((el) => {
        el.hidden = el.id !== `page-${page}`;
    });

    const activeNav = NAV_GROUP[page] || page;
    document.querySelectorAll(".sidebar-nav .nav-item[data-page]").forEach((btn) => {
        btn.classList.toggle("is-active", btn.dataset.page === activeNav);
    });

    document.getElementById("page-title").textContent = TOP_BAR_TITLES[page] || "";

    const loader = window.pageLoaders[page];
    if (loader) loader(opts);
}

window.navigate = navigate;
window.registerPage = registerPage;

// --- List + search ----------------------------------------------------------

let searchTimer = null;
function onSearchInput(event) {
    currentSearch = event.target.value;
    clearTimeout(searchTimer);
    searchTimer = setTimeout(loadQuestions, 150);
}

async function loadQuestions() {
    const url = currentSearch.trim()
        ? `${API_BASE}?search=${encodeURIComponent(currentSearch.trim())}`
        : API_BASE;

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Request failed: ${response.status}`);
        render(await response.json());
    } catch (err) {
        console.error("Failed to load questions", err);
        render([]);
    }
}

function render(questions) {
    els.count.textContent = String(questions.length);

    if (questions.length === 0) {
        els.table.hidden = true;
        renderEmptyState();
        els.emptyState.hidden = false;
        return;
    }

    els.emptyState.hidden = true;
    els.table.hidden = false;
    els.tbody.innerHTML = "";
    for (const q of questions) {
        els.tbody.appendChild(buildRow(q));
    }
}

function renderEmptyState() {
    if (currentSearch.trim()) {
        els.emptyTitle.textContent = "No questions found";
        els.emptyText.textContent = `No questions match "${currentSearch.trim()}".`;
    } else {
        els.emptyTitle.textContent = "No questions yet";
        els.emptyText.textContent = "Get started by adding your first question.";
    }
}

function buildRow(question) {
    const tr = document.createElement("tr");
    tr.dataset.id = question.id;

    const questionCell = document.createElement("td");
    questionCell.className = "question-text";
    questionCell.textContent = question.question;

    const difficultyCell = document.createElement("td");
    difficultyCell.appendChild(buildDifficultyBadge(question.difficulty));

    const actionsCell = document.createElement("td");
    actionsCell.className = "col-actions";

    const editBtn = document.createElement("button");
    editBtn.type = "button";
    editBtn.className = "btn-row-edit";
    editBtn.textContent = "Edit";
    editBtn.addEventListener("click", () => openEdit(question));

    const delBtn = document.createElement("button");
    delBtn.type = "button";
    delBtn.className = "btn-danger-link";
    delBtn.textContent = "Del";
    delBtn.addEventListener("click", () => openDelete(question));

    actionsCell.appendChild(editBtn);
    actionsCell.appendChild(delBtn);

    tr.appendChild(questionCell);
    tr.appendChild(difficultyCell);
    tr.appendChild(actionsCell);
    return tr;
}

function buildDifficultyBadge(difficulty) {
    const span = document.createElement("span");
    const level = (difficulty || "Medium").toLowerCase();
    span.className = `difficulty-badge difficulty-${level}`;
    span.textContent = difficulty || "Medium";
    return span;
}

// --- Editor modal (add / edit) ----------------------------------------------

function openAdd() {
    editingId = null;
    els.editorTitle.textContent = "Add Question";
    resetForm();
    els.editorOverlay.hidden = false;
    document.getElementById("f-question").focus();
}

function openEdit(question) {
    editingId = question.id;
    els.editorTitle.textContent = "Edit Question";
    resetForm();
    els.editorForm.elements.question.value = question.question;
    els.editorForm.elements.a.value = question.a;
    els.editorForm.elements.b.value = question.b;
    els.editorForm.elements.c.value = question.c;
    els.editorForm.elements.d.value = question.d;
    els.editorForm.elements.correct.value = question.correct;
    els.editorForm.elements.difficulty.value = question.difficulty;
    els.editorOverlay.hidden = false;
    document.getElementById("f-question").focus();
}

function closeEditor() {
    els.editorOverlay.hidden = true;
    editingId = null;
}

function resetForm() {
    els.editorForm.reset();
    els.editorForm.elements.correct.value = "A";
    els.editorForm.elements.difficulty.value = "Medium";
    clearErrors();
}

function clearErrors() {
    els.formError.hidden = true;
    els.formError.textContent = "";
    for (const name of FIELD_NAMES) {
        const errEl = els.editorForm.querySelector(`[data-error-for="${name}"]`);
        if (errEl) {
            errEl.hidden = true;
            errEl.textContent = "";
            errEl.closest(".field").classList.remove("has-error");
        }
    }
}

function showFieldErrors(fields) {
    for (const [name, message] of Object.entries(fields)) {
        const errEl = els.editorForm.querySelector(`[data-error-for="${name}"]`);
        if (errEl) {
            errEl.textContent = message;
            errEl.hidden = false;
            errEl.closest(".field").classList.add("has-error");
        }
    }
}

function showFormError(message) {
    els.formError.textContent = message;
    els.formError.hidden = false;
}

async function onEditorSubmit(event) {
    event.preventDefault();
    clearErrors();

    const payload = {
        question: els.editorForm.elements.question.value,
        a: els.editorForm.elements.a.value,
        b: els.editorForm.elements.b.value,
        c: els.editorForm.elements.c.value,
        d: els.editorForm.elements.d.value,
        correct: els.editorForm.elements.correct.value,
        difficulty: els.editorForm.elements.difficulty.value,
    };

    const isEdit = editingId !== null;
    const url = isEdit ? `${API_BASE}/${editingId}` : API_BASE;
    const method = isEdit ? "PUT" : "POST";

    try {
        const response = await fetch(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        if (response.ok) {
            closeEditor();
            await loadQuestions();
            return;
        }

        const body = await response.json().catch(() => ({}));
        if (response.status === 400 && body.fields) {
            showFieldErrors(body.fields);
            showFormError("Please fix the highlighted fields.");
        } else {
            showFormError(body.error || "Could not save the question. Please try again.");
        }
    } catch (err) {
        console.error("Save failed", err);
        showFormError("Network error. Please try again.");
    }
}

// --- Delete flow ------------------------------------------------------------

function openDelete(question) {
    pendingDeleteId = question.id;
    els.deleteOverlay.hidden = false;
}

function closeDelete() {
    els.deleteOverlay.hidden = true;
    pendingDeleteId = null;
}

async function confirmDelete() {
    if (pendingDeleteId === null) return;
    const id = pendingDeleteId;

    try {
        const response = await fetch(`${API_BASE}/${id}`, { method: "DELETE" });
        if (!response.ok && response.status !== 404) {
            throw new Error(`Delete failed: ${response.status}`);
        }
    } catch (err) {
        console.error("Delete failed", err);
    } finally {
        closeDelete();
        await loadQuestions();
    }
}
