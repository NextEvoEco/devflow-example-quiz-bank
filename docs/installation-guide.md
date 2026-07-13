# Installation Guide — Prerequisites for `refactor/java-react-postgre`

This branch targets **Java 21 + Spring Boot 3**, **React 18 + TypeScript (Vite)**, and
**PostgreSQL 16+ (Flyway)**. None of the backend/database prerequisites are bundled with
the repository — install them once before running the implementation pass or starting
the app.

Target OS below is **Windows** (commands use `winget` / PowerShell); a Docker
alternative is given for PostgreSQL.

---

## 1. What You Need

| Tool                        | Version                | Why                                                  | Check command                     |
| --------------------------- | ---------------------- | ---------------------------------------------------- | --------------------------------- |
| JDK (Temurin or equivalent) | 21+ (LTS)              | build & run the Spring Boot backend                  | `java -version`                   |
| Node.js + npm               | Node 24+ / npm 11+     | build the React frontend (Vite)                      | `node --version`, `npm --version` |
| PostgreSQL                  | 16+                    | application database (`quiz_bank`)                   | `psql --version` or `docker ps`   |
| Maven                       | none required globally | the project uses the `mvnw` wrapper; a JDK is enough | `./mvnw -v` (after bootstrap)     |

> Note: the Maven wrapper (`mvnw`) ships with the backend project once o01/t01 is
> implemented (e.g. generated via Spring Initializr). No global Maven install is needed;
> only the JDK must be present.

---

## 2. Install JDK 21

```powershell
winget install EclipseAdoptium.Temurin.21.JDK
```

Then open a **new** terminal and verify:

```powershell
java -version
# expected: openjdk version "21.x.x" ...
```

If `java` is not found, check that the installer added it to `PATH`
(`%ProgramFiles%\Eclipse Adoptium\jdk-21...\bin`) and that `JAVA_HOME` points at the JDK
directory (some tools require it):

```powershell
[Environment]::GetEnvironmentVariable("JAVA_HOME", "Machine")
```

---

## 3. Install Node.js (verify only, if already present)

```powershell
node --version   # need 24+
npm --version    # need 11+
```

If missing:

```powershell
winget install OpenJS.NodeJS.LTS
```

---

## 4. Install PostgreSQL 16+

Choose **one** of the two options.

### Option A — native Windows service

```powershell
winget install PostgreSQL.PostgreSQL.16
```

During/after install, note the superuser (`postgres`) password you set. The service
runs automatically; manage it with `services.msc` (service name like
`postgresql-x64-16`).

### Option B — Docker container

```powershell
docker run --name quiz-bank-pg -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:16
```

Data persists inside the container; add `-v quiz_bank_pgdata:/var/lib/postgresql/data`
for a named volume if you want it to survive container recreation.

---

## 5. Create the Application Database

Connect as the superuser and create a dedicated role + database:

```powershell
# native install (psql is under the PostgreSQL bin directory, or added to PATH):
psql -U postgres -h 127.0.0.1

# docker:
docker exec -it quiz-bank-pg psql -U postgres
```

Then in `psql`:

```sql
CREATE ROLE quiz WITH LOGIN PASSWORD 'quiz';
CREATE DATABASE quiz_bank OWNER quiz;
\q
```

Verify the application role can connect:

```powershell
psql -U quiz -h 127.0.0.1 -d quiz_bank -c "SELECT 1;"
# docker: docker exec -it quiz-bank-pg psql -U quiz -d quiz_bank -c "SELECT 1;"
```

---

## 6. Connection Configuration

The backend reads its datasource from Spring configuration. Local default (to be set in
`backend/src/main/resources/application.properties` by the implementation pass):

```properties
spring.datasource.url=jdbc:postgresql://127.0.0.1:5432/quiz_bank
spring.datasource.username=quiz
spring.datasource.password=quiz
server.port=5000
```

Override without editing files via environment variables when needed:

```powershell
$env:SPRING_DATASOURCE_URL      = "jdbc:postgresql://127.0.0.1:5432/quiz_bank"
$env:SPRING_DATASOURCE_USERNAME = "quiz"
$env:SPRING_DATASOURCE_PASSWORD = "quiz"
```

Schema creation is fully automatic: Flyway applies the migrations in
`backend/src/main/resources/db/migration/` on application start — no manual DDL.

---

## 7. Start the App (after the implementation pass)

```powershell
# 1) build the frontend
cd frontend
npm install
npm run build

# 2) run the backend (serves API + built frontend)
cd ..\backend
.\mvnw spring-boot:run
```

Open `http://127.0.0.1:5000`.

Tests:

```powershell
cd backend;  .\mvnw test      # backend (JUnit 5)
cd frontend; npm test         # frontend (vitest)
```

---

## 8. Seed Data (optional)

The shared demo dataset (50 world-geography questions, 3 quizzes) is checked in as
`data/quiz_bank.db` (SQLite) with the **same logical schema** as PostgreSQL
(`questions.option_a..option_d`, `correct`, `difficulty`, …).

After Flyway has created the schema (start the app once), import into PostgreSQL:

```powershell
# Requires Docker container quiz-bank-pg (see §4 Option B) or edit PSQL_CMD in the script.
python scripts/import_seed_from_sqlite.py
```

Verify:

```powershell
# expect ~50
python -c "import urllib.request,json; print(len(json.load(urllib.request.urlopen('http://127.0.0.1:5000/api/questions'))))"
```

The SQLite file is a **seed source only** — the running app never opens it. After a
successful import and UI check, `data/quiz_bank.db` may be removed from the branch.

---

## 9. Troubleshooting

- **`java` not found after install** — open a new terminal; installers update `PATH`
  for new sessions only.
- **Port 5432 already in use** — another PostgreSQL instance is running; reuse it
  (adjust the URL) or change the container's published port (`-p 5433:5432`).
- **Port 5000 already in use** — a previous app process is still listening. Find and
  stop it: `netstat -ano | findstr :5000`, then `taskkill /PID <pid> /F`. Stale
  processes serving old code are a known trap in this repository.
- **Flyway checksum/version errors after switching branches** — the database keeps the
  migration history. For a demo reset, drop and recreate the database
  (`DROP DATABASE quiz_bank; CREATE DATABASE quiz_bank OWNER quiz;`).
