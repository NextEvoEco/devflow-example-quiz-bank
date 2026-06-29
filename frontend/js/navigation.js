const PAGE_CONFIG = {
  questions: {
    pageId: "page-questions",
    title: "Questions",
    navTarget: "questions",
  },
  quizList: {
    pageId: "page-quiz-list",
    title: "Quizzes",
    navTarget: "quizList",
  },
  quizCreate: {
    pageId: "page-quiz-builder",
    title: "Quiz Builder",
    navTarget: "quizList",
  },
};

const navigationState = {
  currentPage: "questions",
  quizBuilderQuizId: null,
};

function getPageFromHash() {
  const hash = window.location.hash.replace(/^#/, "");
  if (!hash || hash === "questions") {
    return { page: "questions", quizId: null };
  }
  if (hash === "quizList") {
    return { page: "quizList", quizId: null };
  }
  if (hash === "quizCreate") {
    return { page: "quizCreate", quizId: null };
  }
  const editMatch = hash.match(/^quizCreate\/(\d+)$/);
  if (editMatch) {
    return { page: "quizCreate", quizId: Number(editMatch[1]) };
  }
  return { page: "questions", quizId: null };
}

function updateHash(page, quizId = null) {
  if (page === "questions") {
    window.location.hash = "questions";
    return;
  }
  if (page === "quizList") {
    window.location.hash = "quizList";
    return;
  }
  if (page === "quizCreate" && quizId) {
    window.location.hash = `quizCreate/${quizId}`;
    return;
  }
  if (page === "quizCreate") {
    window.location.hash = "quizCreate";
  }
}

function setActiveNav(navTarget) {
  document.querySelectorAll("[data-nav-target]").forEach((button) => {
    const isActive = button.dataset.navTarget === navTarget;
    button.classList.toggle("is-active", isActive);
  });
}

function showPage(page, quizId = null) {
  const config = PAGE_CONFIG[page];
  if (!config) {
    return;
  }

  navigationState.currentPage = page;
  navigationState.quizBuilderQuizId = quizId;

  document.querySelectorAll(".page-view").forEach((section) => {
    section.hidden = true;
  });

  const pageElement = document.getElementById(config.pageId);
  if (pageElement) {
    pageElement.hidden = false;
  }

  const topbarTitle = document.getElementById("topbar-title");
  if (topbarTitle) {
    topbarTitle.textContent = config.title;
  }

  setActiveNav(config.navTarget);

  if (page === "questions" && typeof window.refreshQuestionBank === "function") {
    window.refreshQuestionBank();
  }
  if (page === "quizList" && typeof window.refreshQuizList === "function") {
    window.refreshQuizList();
  }
  if (page === "quizCreate" && typeof window.refreshQuizBuilder === "function") {
    window.refreshQuizBuilder(quizId);
  }
}

function navigateToPage(page, options = {}) {
  const quizId = options.quizId ?? null;
  updateHash(page, quizId);
  showPage(page, quizId);
}

function initNavigation() {
  document.querySelectorAll("[data-nav-target]").forEach((button) => {
    button.addEventListener("click", () => {
      const target = button.dataset.navTarget;
      if (target === "questions") {
        navigateToPage("questions");
      }
      if (target === "quizList") {
        navigateToPage("quizList");
      }
    });
  });

  const quizBuilderBackBtn = document.getElementById("quiz-builder-back-btn");
  if (quizBuilderBackBtn) {
    quizBuilderBackBtn.addEventListener("click", () => navigateToPage("quizList"));
  }

  window.addEventListener("hashchange", () => {
    const { page, quizId } = getPageFromHash();
    showPage(page, quizId);
  });

  const { page, quizId } = getPageFromHash();
  showPage(page, quizId);
}

window.navigateToPage = navigateToPage;

document.addEventListener("DOMContentLoaded", initNavigation);
