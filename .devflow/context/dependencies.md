# Dependencies Context

## Purpose

Use this file to record important project dependencies that AI should be aware of.

## When To Fill

Fill this file when dependency choices, critical integrations, or version constraints are confirmed.

## Current Status

The V1 implementation is already running with a small confirmed dependency set.

This file should reflect the live codebase first, while still noting where later expansion may add dependencies.

### Core Dependencies

Confirmed dependency categories:

- JDK 21+ runtime (backend)
- Node.js runtime (frontend build toolchain only)
- PostgreSQL database service (local install or Docker)
- browser runtime for the frontend

Currently selected on this branch:

- Spring Boot 3.x (web, jdbc) for the local web server and data access
- Flyway for schema migrations
- PostgreSQL JDBC driver
- JUnit 5 + Spring Boot Test for backend tests
- React 18 + TypeScript, Vite, vitest for the frontend

### External Services

None are currently in scope for V1.

There is no confirmed dependency on:

- cloud APIs
- authentication providers
- hosted databases
- payment services
- messaging platforms

### Version Constraints

Confirmed versions:

- Java 21+ (LTS), Spring Boot 3.x, Flyway, PostgreSQL 16+
- Node.js 24+ / npm 11+
- React 18.x, Vite 5+/6+, vitest (versions pinned in `pom.xml` / `package.json` when implemented)

### Upgrade Risks

Potential future risks to track as the product grows:

- Spring Boot major-version upgrades after the API shape is established
- PostgreSQL/Flyway migration ordering once multiple migrations exist
- React/Vite major-version upgrades once components and build config are established

At the moment, these are forward-looking cautions rather than active blockers.

### Notes

- keep dependency choices lightweight for V1
- avoid unnecessary libraries before a new version milestone truly needs them
- record every chosen dependency here once it becomes part of the implementation
- when target specs expand ahead of code, do not list future dependencies here until they are actually adopted
