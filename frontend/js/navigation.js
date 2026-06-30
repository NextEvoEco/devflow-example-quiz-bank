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
  examList: {
    pageId: "page-exam-list",
    title: "Available Exams",
    navTarget: "examList",
  },
  examTaking: {
    pageId: "page-exam-taking",
    title: "Exam",
    navTarget: "examList",
  },
  examResults: {
    pageId: "page-exam-results",
    title: "Exam Results",
    navTarget: "examList",
  },
};

const navigationState = {
  currentPage: "questions",
  quizBuilderQuizId: null,
  examQuizId: null,
};

function getPageFromHash() {
  const hash = window.location.hash.replace(/^#/, "");
  if (!hash || hash === "questions") {
    return { page: "questions", quizId: null, examQuizId: null };
  }
  if (hash === "quizList") {
    return { page: "quizList", quizId: null, examQuizId: null };
  }
  if (hash === "quizCreate") {
    return { page: "quizCreate", quizId: null, examQuizId: null };
  }
  if (hash === "examList") {
    return { page: "examList", quizId: null, examQuizId: null };
  }
  if (hash === "examResults") {
    return { page: "examResults", quizId: null, examQuizId: null };
  }
  const editMatch = hash.match(/^quizCreate\/(\d+)$/);
  if (editMatch) {
    return { page: "quizCreate", quizId: Number(editMatch[1]), examQuizId: null };
  }
  const examMatch = hash.match(/^examTaking\/(\d+)$/);
  if (examMatch) {
    return { page: "examTaking", quizId: null, examQuizId: Number(examMatch[1]) };
  }
  return { page: "questions", quizId: null, examQuizId: null };
}

function updateHash(page, quizId = null, examQuizId = null) {
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
    return;
  }
  if (page === "examList") {
    window.location.hash = "examList";
    return;
  }
  if (page === "examResults") {
    window.location.hash = "examResults";
    return;
  }
  if (page === "examTaking" && examQuizId) {
    window.location.hash = `examTaking/${examQuizId}`;
  }
}

function setActiveNav(navTarget) {
  document.querySelectorAll("[data-nav-target]").forEach((button) => {
    const isActive = button.dataset.navTarget === navTarget;
    button.classList.toggle("is-active", isActive);
  });
}

function showPage(page, quizId = null, examQuizId = null) {
  const config = PAGE_CONFIG[page];
  if (!config) {
    return;
  }

  const previousPage = navigationState.currentPage;

  navigationState.currentPage = page;
  navigationState.quizBuilderQuizId = quizId;
  navigationState.examQuizId = examQuizId;

  if (
    previousPage === "examTaking" &&
    page !== "examTaking" &&
    page !== "examResults" &&
    typeof window.abandonExamSession === "function"
  ) {
    window.abandonExamSession();
  }

  if (
    previousPage === "examResults" &&
    page !== "examResults" &&
    page !== "examTaking" &&
    typeof window.clearExamResultsSession === "function"
  ) {
    window.clearExamResultsSession();
  }

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
  if (page === "examList" && typeof window.refreshExamList === "function") {
    window.refreshExamList();
  }
  if (page === "examTaking" && typeof window.refreshExamTaking === "function") {
    if (window.examState) {
      window.examState.currentExamQuizId = examQuizId;
    }
    window.refreshExamTaking(examQuizId);
  }
  if (page === "examResults" && typeof window.refreshExamResults === "function") {
    window.refreshExamResults();
  }
}

function navigateToPage(page, options = {}) {
  if (page === "examTaking") {
    const examQuizId = options.quizId ?? options.examQuizId ?? null;
    updateHash(page, null, examQuizId);
    showPage(page, null, examQuizId);
    return;
  }

  if (page === "examResults") {
    updateHash(page, null, null);
    showPage(page, null, null);
    return;
  }

  const quizId = options.quizId ?? null;
  updateHash(page, quizId, null);
  showPage(page, quizId, null);
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
      if (target === "examList") {
        navigateToPage("examList");
      }
    });
  });

  const quizBuilderBackBtn = document.getElementById("quiz-builder-back-btn");
  if (quizBuilderBackBtn) {
    quizBuilderBackBtn.addEventListener("click", () => navigateToPage("quizList"));
  }

  window.addEventListener("hashchange", () => {
    const { page, quizId, examQuizId } = getPageFromHash();
    showPage(page, quizId, examQuizId);
  });

  const { page, quizId, examQuizId } = getPageFromHash();
  showPage(page, quizId, examQuizId);
}

window.navigateToPage = navigateToPage;

document.addEventListener("DOMContentLoaded", initNavigation);
