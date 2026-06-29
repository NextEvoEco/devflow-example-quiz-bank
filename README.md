# DevFlow Example - Quiz Bank

> A reference implementation demonstrating how DevFlow structures AI-assisted software development through a real project.

This repository is the official reference implementation of **DevFlow**.

Rather than explaining the workflow through abstract concepts, this project demonstrates how DevFlow artifacts evolve while building a complete Quiz Bank application from the initial idea to a working product.

Every development decision is preserved as part of the project itself, allowing both humans and AI to continue development across sessions without relying on conversation history.

---

# Purpose

This repository demonstrates how DevFlow organizes software development into persistent project artifacts.

Instead of treating AI conversations as project memory, DevFlow stores project state directly inside the repository.

By following this example, you can see:

* How a project starts from an initial intent
* How requirements are clarified through interviews
* How objectives become executable tasks
* How execution progress is tracked
* How project context remains independent from conversations
* How development decisions are preserved as evidence

---

# What This Repository Demonstrates

This project builds a simple local Quiz Bank application.

The application itself is intentionally small.

The primary purpose is to demonstrate the DevFlow workflow rather than application complexity.

Current development roadmap:

* V1 - Question Bank
* V2 - Quiz Builder
* V3 - Online Exam

Each version introduces additional DevFlow artifacts while keeping the application understandable.

---

# Current Status

Current implemented scope:

* V1 - Question Bank
* V2 - Quiz Builder

Planned next scope:

* V3 - Online Exam

The current application supports:

* Question Bank CRUD
* SQLite persistence
* Quiz Builder CRUD
* Selecting existing questions into quizzes
* Manual question reordering inside quizzes
* Quiz preview before save

The current application does not yet support:

* Online Exam runtime
* Automatic sample-data import on startup

---

# Repository Structure

```text
.devflow/
    intent/         Project intent for each iteration
    interview/      Requirement clarification records
    objective/      Version objectives
    tasks/          Individual executable tasks
    evidence/       Development evidence and decision records
    context/        Project environment
                        - architecture
                        - technology stack
                        - conventions
                        - dependencies
    status.md       Execution progress
    memory.md       Durable cross-session knowledge
    roles/          AI role definitions
    skills/         AI skill definitions
    templates/      Artifact templates

backend/
    Flask application, routes, validation, repositories, and SQLite bootstrap

frontend/
    Plain HTML, CSS, and JavaScript UI

data/
    Local SQLite database files

docs/
    Supporting documentation and verification guides

example_data/
    Manual demo data for Question Bank and Quiz Builder testing

tests/
    Automated test suite
```

---

# Example Data

The app starts with an empty Question Bank by default.

No sample questions or quizzes are auto-imported at startup.

Use the files in `example_data/` for manual testing:

* `world-geography-basic-50.md` - question-bank sample data for manual entry
* `quiz-builder-world-geography-3.md` - 3-question quiz sample
* `quiz-builder-world-geography-5.md` - 5-question quiz sample
* `quiz-builder-world-geography-10.md` - 10-question quiz sample

The quiz sample files describe:

* quiz name
* question count
* which existing Question Bank items to select
* the intended question order in Quiz Builder

---

# Getting Started

## Requirements

* Python 3.13 or compatible local Python environment
* `pip` for dependency installation

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run The App

Start the application from the repository root:

```bash
py -m backend
```

Default local URL:

```text
http://127.0.0.1:5000
```

On first run, the app creates the SQLite database automatically at `data/quiz_bank.db`.

---

# Testing

Run the automated test suite from the repository root:

```bash
py -m pytest tests/ -v
```

Additional verification guides:

* [docs/v1-verification.md](docs/v1-verification.md) for Question Bank V1 verification
* [docs/o02-verification.md](docs/o02-verification.md) for Quiz Builder V1 verification
* [docs/getting-started.md](docs/getting-started.md) for DevFlow reading and startup guidance

---

# Development Philosophy

DevFlow separates **project state** from **AI conversations**.

Instead of depending on a chat history, every important decision is externalized into structured Markdown artifacts.

This allows development to continue across:

* new AI sessions
* different AI models
* different engineers
* different development tools

without reconstructing project context from scratch.

---

# Learning Path

The recommended reading order is:

1. `.devflow/status.md` - current execution state
2. `.devflow/intent/` - project intent artifacts
3. `.devflow/interview/` - requirement clarification records
4. `.devflow/objective/` - confirmed objectives
5. `.devflow/tasks/` - individual executable tasks
6. `.devflow/evidence/` - development decisions and outcomes
7. `.devflow/context/` - project environment reference

Following this order shows how an idea gradually becomes executable software.

If you are new to DevFlow and want to apply it to your own project, see [docs/getting-started.md](docs/getting-started.md).

---

# Relationship to DevFlow

This repository is a reference implementation.

The DevFlow framework itself is maintained separately.

**DevFlow Framework**

[https://github.com/NextEvoEco/devflow](https://github.com/NextEvoEco/devflow)

This repository focuses on demonstrating how DevFlow is applied in practice.

---

# License

MIT License
