# 03 — Deployment

How to build, run, verify, and reset the local Quiz Bank application.

This project is designed as a **local web app** (no cloud hosting requirement).
“Deployment” here means starting a complete instance on one machine.

Commands below use **bash**.

---

## Architecture at runtime

```text
Browser  --->  Spring Boot (:5000)
                 |-- /api/**     REST controllers
                 |-- /           React SPA (frontend/dist)
                 `-- JDBC        PostgreSQL (quiz_bank)
```

Flyway runs on startup and applies pending migrations.

---

## Build

### Frontend

```bash
cd frontend
npm install
npm run build
```

Output: `frontend/dist/` (git-ignored).

### Backend

No separate package step is required for local run. Maven compiles on
`spring-boot:run` or `package`:

```bash
cd backend
./mvnw -q -DskipTests package
```

Runnable jar (optional):

```bash
./mvnw -q -DskipTests package
java -jar target/quiz-bank-0.0.1-SNAPSHOT.jar
```

When using the jar, set `QUIZBANK_FRONTEND_DIST` to an absolute path of `frontend/dist`
if the relative default does not resolve:

```bash
export QUIZBANK_FRONTEND_DIST="$(pwd)/../frontend/dist"
java -jar target/quiz-bank-0.0.1-SNAPSHOT.jar
```

---

## Run (recommended)

From the repository root:

```bash
# 1) Build SPA
cd frontend
npm install
npm run build

# 2) Start API + SPA
cd ../backend
./mvnw spring-boot:run
```

Open: `http://127.0.0.1:5000`

Prerequisites (see [01-install.md](01-install.md)):

- JDK 21+
- PostgreSQL with database `quiz_bank` and role `quiz` / password `quiz`
- Node.js 24+ for the frontend build

---

## Verify

### Health

```bash
curl -s http://127.0.0.1:5000/api/health
# expect: "status":"ok"
```

### SPA

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:5000/
# expect: 200

curl -s http://127.0.0.1:5000/ | head
# expect HTML with title Quiz Bank
```

### Automated tests

```bash
cd backend
./mvnw test

cd ../frontend
npm test
```

### Optional seed

```bash
python3 scripts/import_seed_from_sqlite.py
```

Then confirm questions are available:

```bash
curl -s http://127.0.0.1:5000/api/questions | python3 -c "import sys,json; print(len(json.load(sys.stdin)))"
# expect: ~50 after seed import
```

---

## Process management

### Stop the app

- If started in a terminal: `Ctrl+C`
- If a stale process holds port 5000:

```bash
lsof -i :5000
kill <pid>
# force if needed:
kill -9 <pid>
```

### Restart after frontend changes

Rebuild the SPA, then restart Spring Boot (safest is rebuild + restart):

```bash
cd frontend
npm run build
cd ../backend
./mvnw spring-boot:run
```

---

## Database reset

For a clean demo database (drops all app data and Flyway history):

```bash
psql -U postgres -h 127.0.0.1 <<'SQL'
DROP DATABASE quiz_bank;
CREATE DATABASE quiz_bank OWNER quiz;
SQL
```

Start the app again to re-run Flyway, then optionally re-import seed data.

---

## Configuration in deployed/local instances

Override connection settings with environment variables (see
[02-configuration.md](02-configuration.md)):

```bash
export SPRING_DATASOURCE_URL=jdbc:postgresql://127.0.0.1:5432/quiz_bank
export SPRING_DATASOURCE_USERNAME=quiz
export SPRING_DATASOURCE_PASSWORD=quiz
export SERVER_PORT=5000
```

Keep credentials out of source control for any shared environment.

---

## Out of scope

This branch does not provide:

- Docker Compose for the full app stack (PostgreSQL container is optional only)
- Cloud deployment manifests
- Authentication / HTTPS termination
- Multi-instance / clustered setup

---

## Related docs

- [01-install.md](01-install.md)
- [02-configuration.md](02-configuration.md)
- [04-user-guide.md](04-user-guide.md)
- [05-api-reference.md](05-api-reference.md)
