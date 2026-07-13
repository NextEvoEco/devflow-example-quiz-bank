# 01 — Install

Install the tools required to build and run Quiz Bank on a local machine.

**Stack:** Java 21 + Spring Boot 3, React 18 + TypeScript (Vite), PostgreSQL 16+ (Flyway).

Commands below use **bash**.

---

## Prerequisites

| Tool                        | Version               | Purpose                               | Check                             |
| --------------------------- | --------------------- | ------------------------------------- | --------------------------------- |
| JDK (Temurin or equivalent) | 21+                   | Build and run the Spring Boot backend | `java -version`                   |
| Node.js + npm               | Node 24+ / npm 11+    | Build the React frontend              | `node --version`, `npm --version` |
| PostgreSQL                  | 16+                   | Application database                  | `psql --version` or `docker ps`   |
| Maven                       | not required globally | Use the project `mvnw` wrapper        | `./mvnw -v` (from `backend/`)     |

Optional for seed import: Python 3 (`scripts/import_seed_from_sqlite.py`).

---

## 1. Install JDK 21

### macOS (Homebrew)

```bash
brew install --cask temurin@21
java -version
# expected: openjdk version "21.x.x" ...
```

### Linux (example: Temurin apt)

Follow your distro’s JDK 21 instructions, then confirm:

```bash
java -version
```

If `java` is not found, set `JAVA_HOME` and update `PATH`:

```bash
export JAVA_HOME=/path/to/jdk-21
export PATH="$JAVA_HOME/bin:$PATH"
```

### Windows (Git Bash / WSL)

Prefer installing Temurin 21 via the OS installer or `winget`, then use Git Bash or WSL with `java` on `PATH`. Verify with `java -version`.

---

## 2. Install Node.js

```bash
node --version   # need 24+
npm --version    # need 11+
```

If missing (Homebrew example):

```bash
brew install node
```

---

## 3. Install PostgreSQL 16+

Choose one option.

### Option A — native package

```bash
# macOS
brew install postgresql@16
brew services start postgresql@16

# Debian/Ubuntu (example)
# sudo apt install postgresql-16
```

### Option B — Docker

```bash
docker run --name quiz-bank-pg \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d postgres:16
```

Add `-v quiz_bank_pgdata:/var/lib/postgresql/data` if you want data to survive container recreation.

---

## 4. Create the application database

Connect as the PostgreSQL superuser:

```bash
# native
psql -U postgres -h 127.0.0.1

# Docker
docker exec -it quiz-bank-pg psql -U postgres
```

Then run:

```sql
CREATE ROLE quiz WITH LOGIN PASSWORD 'quiz';
CREATE DATABASE quiz_bank OWNER quiz;
\q
```

Verify:

```bash
psql -U quiz -h 127.0.0.1 -d quiz_bank -c "SELECT 1;"
# Docker:
docker exec -it quiz-bank-pg psql -U quiz -d quiz_bank -c "SELECT 1;"
```

---

## 5. Clone and install project dependencies

```bash
git clone <repository-url>
cd devflow-example-quiz-bank

cd frontend
npm install
cd ../backend
./mvnw -v
```

No global Maven install is required; the wrapper downloads Maven on first use.

On Windows Git Bash, `./mvnw` works if the file is executable; otherwise use `./mvnw.cmd` from cmd, or run via Git Bash after `chmod +x mvnw`.

---

## 6. First start (smoke check)

```bash
cd frontend
npm run build

cd ../backend
./mvn spring-boot:run
```

Open `http://127.0.0.1:5000`. Flyway creates the schema automatically on first start.

Health check:

```bash
curl -s http://127.0.0.1:5000/api/health
```

---

## 7. Optional demo seed

After the app has started once (so Flyway migrations exist):

```bash
python scripts/import_seed_from_sqlite.py
# or: python3 scripts/import_seed_from_sqlite.py
```

This loads ~50 geography questions and 3 quizzes from `data/quiz_bank.db` into PostgreSQL.
The SQLite file is a seed source only; the running app never opens it.

---

## Troubleshooting

| Symptom                                      | What to try                                             |
| -------------------------------------------- | ------------------------------------------------------- |
| `java` not found                             | Set `JAVA_HOME` / `PATH`; open a new shell              |
| Port 5432 in use                             | Reuse the existing instance or map another host port    |
| Port 5000 in use                             | Stop the old process: `lsof -i :5000` then `kill <pid>` |
| Flyway checksum errors after branch switches | Drop and recreate `quiz_bank`                           |

See also: [02-configuration.md](02-configuration.md), [03-deployment.md](03-deployment.md).
