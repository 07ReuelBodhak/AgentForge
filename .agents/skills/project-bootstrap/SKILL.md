---
name: project-bootstrap
description: Guidelines for establishing repository structures, isolated language environments, and dependency manifests.
---

# Project Bootstrap Guidelines

Use this skill when initializing new repositories or configuring service environments.

## 1. Structure Derivation
- Derive structure directly from `docs/project-context.md` (# Project Structure).
- **Full-stack**: Separate services cleanly (e.g. `frontend/` and `backend/`).
- **Single-service**: Cohesive module layout.
- **Monorepo**: Workspace layout (e.g. `packages/*` or `apps/*`).
- Do not dump multi-service code into root.

## 2. Environment & Manifest Bootstrap
Every service must establish its local environment and dependency manifest:
- **Python**: Create `.venv` (`python -m venv .venv`), install packages via `.venv/Scripts/pip`, maintain `requirements.txt`.
- **Node/TS**: Create `package.json` with explicit dependencies and lockfile.
- **Rust**: Create `Cargo.toml`.
- **Go**: Create `go.mod` / `go.sum`.
- Never install packages into global interpreters or commit unmanifested dependencies.

## 3. Secret & Database Safety
- Provide `.env.example` templates with non-sensitive dummy placeholders.
- Tests must target isolated test connection strings (`TEST_DATABASE_URL`), never production.
