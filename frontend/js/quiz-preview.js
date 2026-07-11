// Quiz Preview (o02/t05).
// Defines window.openQuizPreview(draft) — a modal that shows a quiz's full
// content (each question's text, options A-D, and the correct answer) in order.
// Works from the builder's in-memory draft; does not require a save.

(() => {
    const OPTION_LETTERS = ["A", "B", "C", "D"];

    const p = {};

    document.addEventListener("DOMContentLoaded", () => {
        p.overlay = document.getElementById("preview-overlay");
        p.title = document.getElementById("preview-title");
        p.body = document.getElementById("preview-body");

        document.getElementById("preview-close").addEventListener("click", close);
        document.getElementById("preview-close-btn").addEventListener("click", close);
        p.overlay.addEventListener("click", (e) => {
            if (e.target === p.overlay) close();
        });
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape") close();
        });

        // Expose the hook the Quiz Builder's Preview button calls.
        window.openQuizPreview = open;
    });

    function open(draft = {}) {
        const name = (draft.name || "").trim();
        const questions = draft.questions || [];
        p.title.textContent = name ? `Preview: ${name}` : "Quiz Preview";
        renderBody(questions);
        p.overlay.hidden = false;
    }

    function close() {
        p.overlay.hidden = true;
    }

    function renderBody(questions) {
        p.body.innerHTML = "";

        if (questions.length === 0) {
            const empty = document.createElement("p");
            empty.className = "builder-empty";
            empty.textContent = "No questions to preview.";
            p.body.appendChild(empty);
            return;
        }

        questions.forEach((question, index) => {
            p.body.appendChild(buildQuestion(question, index));
        });
    }

    function buildQuestion(question, index) {
        const card = document.createElement("div");
        card.className = "preview-question";

        const num = document.createElement("span");
        num.className = "preview-q-num";
        num.textContent = `Question ${index + 1}`;

        const text = document.createElement("p");
        text.className = "preview-q-text";
        text.textContent = question.question;

        card.appendChild(num);
        card.appendChild(text);

        const options = document.createElement("ul");
        options.className = "preview-options";
        const correct = (question.correct || "").toUpperCase();

        for (const letter of OPTION_LETTERS) {
            const li = document.createElement("li");
            li.className = "preview-option";
            const isCorrect = correct === letter;
            if (isCorrect) li.classList.add("is-correct");

            const label = document.createElement("span");
            label.className = "preview-opt-label";
            label.textContent = letter;

            const value = document.createElement("span");
            value.className = "preview-opt-text";
            value.textContent = question[letter.toLowerCase()];

            li.appendChild(label);
            li.appendChild(value);

            if (isCorrect) {
                const mark = document.createElement("span");
                mark.className = "preview-correct-mark";
                mark.textContent = "✓ Correct";
                li.appendChild(mark);
            }
            options.appendChild(li);
        }

        card.appendChild(options);
        return card;
    }
})();
