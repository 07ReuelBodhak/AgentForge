# Language Manifests & Environment Isolation Reference

## 1. Dependency Manifest Standards
When introducing or updating libraries, always declare them in the service manifest:
- **Python**: `requirements.txt` or `pyproject.toml` in service root (e.g. `backend/requirements.txt`). Specify version bounds (`fastapi>=0.110.0`, `pytest>=8.0.0`).
- **Node.js / TypeScript**: `package.json` with explicit `dependencies` / `devDependencies`.
- **Go**: `go.mod` and `go.sum`.
- **Rust**: `Cargo.toml` with `[dependencies]`.
- **Java / Kotlin**: `pom.xml` (Maven) or `build.gradle` (Gradle).

## 2. Environment Isolation Patterns
- **Python**: Always use `.venv`. Run commands via `.venv/Scripts/python` (Windows) or `.venv/bin/python` (POSIX). Never use global Python.
- **Node**: Use local `node_modules` and package scripts.
- **Database Isolation**: Tests must target isolated local test databases (e.g. SQLite test file or local test container) via `TEST_DATABASE_URL`. Never target production URLs.

## 3. Dual-Import Compatibility Pattern (Python)
Ensure entrypoints work from both the service folder and the repository root:
```python
import sys
from pathlib import Path

# Add parent directory to sys.path if invoked from service directory
service_dir = Path(__file__).resolve().parent
parent_dir = service_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

try:
    from backend.database import engine
except ImportError:
    from database import engine
```
