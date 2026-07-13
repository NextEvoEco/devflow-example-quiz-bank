# 02 — Configuration

Configuration for the Quiz Bank backend and how the built frontend is served.

Commands below use **bash**.

---

## Configuration file

Primary file:

```text
backend/src/main/resources/application.properties
```

Default contents:

```properties
spring.application.name=quiz-bank
server.port=5000

spring.datasource.url=jdbc:postgresql://127.0.0.1:5432/quiz_bank
spring.datasource.username=quiz
spring.datasource.password=quiz

spring.flyway.enabled=true
spring.flyway.locations=classpath:db/migration

# Path to Vite build output, relative to the backend working directory
quizbank.frontend.dist=../frontend/dist
```

---

## Settings reference

| Property                     | Default                                      | Description                                       |
| ---------------------------- | -------------------------------------------- | ------------------------------------------------- |
| `server.port`                | `5000`                                       | HTTP port for API and SPA                         |
| `spring.datasource.url`      | `jdbc:postgresql://127.0.0.1:5432/quiz_bank` | JDBC URL                                          |
| `spring.datasource.username` | `quiz`                                       | Database role                                     |
| `spring.datasource.password` | `quiz`                                       | Database password                                 |
| `spring.flyway.enabled`      | `true`                                       | Apply migrations on startup                       |
| `spring.flyway.locations`    | `classpath:db/migration`                     | Migration scripts location                        |
| `quizbank.frontend.dist`     | `../frontend/dist`                           | Directory containing Vite `index.html` and assets |

---

## Environment variable overrides

Spring Boot relaxed binding allows overrides without editing the properties file:

| Environment variable         | Maps to                      |
| ---------------------------- | ---------------------------- |
| `SPRING_DATASOURCE_URL`      | `spring.datasource.url`      |
| `SPRING_DATASOURCE_USERNAME` | `spring.datasource.username` |
| `SPRING_DATASOURCE_PASSWORD` | `spring.datasource.password` |
| `SERVER_PORT`                | `server.port`                |
| `QUIZBANK_FRONTEND_DIST`     | `quizbank.frontend.dist`     |

### Example

```bash
export SPRING_DATASOURCE_URL=jdbc:postgresql://127.0.0.1:5432/quiz_bank
export SPRING_DATASOURCE_USERNAME=quiz
export SPRING_DATASOURCE_PASSWORD=quiz
export SERVER_PORT=5000

cd backend
./mvnw spring-boot:run
```

One-shot for a single process:

```bash
SPRING_DATASOURCE_URL=jdbc:postgresql://127.0.0.1:5432/quiz_bank \
SPRING_DATASOURCE_USERNAME=quiz \
SPRING_DATASOURCE_PASSWORD=quiz \
./mvnw spring-boot:run
```

---

## Database and Flyway

- Schema is created and versioned by Flyway migrations under
  `backend/src/main/resources/db/migration/`.
- Do **not** run manual DDL for application tables; restart the app after adding a migration.
- Current migration versions include baseline, `questions`, `quizzes` / `quiz_questions`,
  and `exam_attempts` / `exam_answers`.

If you change databases or switch branches with incompatible migration history:

```bash
psql -U postgres -h 127.0.0.1 <<'SQL'
DROP DATABASE quiz_bank;
CREATE DATABASE quiz_bank OWNER quiz;
SQL
```

Then start the app again so Flyway re-applies all migrations.

---

## Frontend build path

The backend serves the SPA from `quizbank.frontend.dist`.

Expected workflow:

1. `npm run build` in `frontend/` produces `frontend/dist/`.
2. Run Spring Boot from `backend/` so the default relative path `../frontend/dist` resolves.
3. Requests to `/` and static assets under `/assets/...` are served from that directory.
4. API routes under `/api/**` are handled by Spring controllers.

If you run the backend from a different working directory, set
`quizbank.frontend.dist` (or `QUIZBANK_FRONTEND_DIST`) to an absolute path of `frontend/dist`:

```bash
export QUIZBANK_FRONTEND_DIST=/absolute/path/to/frontend/dist
```

---

## Local development notes

- There is no separate Vite reverse-proxy requirement for the shipped mode: build once,
  then use Spring Boot on port 5000.
- Vite `npm run dev` can be used for frontend-only iteration, but API calls expect the
  backend on the same origin in production mode. Prefer the documented build + Spring Boot flow
  for full-stack verification.
- Default credentials (`quiz` / `quiz`) are for local demo only. Change them for any shared
  or non-local environment.

---

## Related docs

- [01-install.md](01-install.md) — prerequisites and first setup
- [03-deployment.md](03-deployment.md) — run, verify, reset
- [05-api-reference.md](05-api-reference.md) — HTTP API
