# Language Manifests & Environment Isolation Reference

## 1. Dependency Minimalism & Evaluation Rules
Before adding ANY third-party library or external package:
1. **Check existing dependencies**: Is a library already installed that can solve this?
2. **Check standard library**: Does the language's standard library or framework already provide this functionality? (e.g. Python `hashlib`/`secrets`/`urllib`, Dart `dart:convert`/`dart:io`).
3. **Assess maintenance overhead**: Is the dependency genuinely justified, or can a 10-line helper function solve it without external risk?
4. **Record justification**: When a dependency is added, explicitly declare the package and the reason in the task report.

## 2. Dependency Manifest Standards by Language
When introducing or updating libraries, always declare them in the service manifest:
- **Python**: `requirements.txt` or `pyproject.toml` in service root (e.g. `backend/requirements.txt`). Specify version bounds (`fastapi>=0.110.0`, `pytest>=8.0.0`).
- **Flutter / Dart**: `pubspec.yaml` under `dependencies` or `dev_dependencies`. Run `flutter pub get`.
- **Node.js / TypeScript**: `package.json` with explicit `dependencies` / `devDependencies` and lockfile.
- **Go**: `go.mod` and `go.sum`.
- **Rust**: `Cargo.toml` with `[dependencies]`.
- **Java / Kotlin**: `pom.xml` (Maven) or `build.gradle` (Gradle).

## 3. Environment Isolation Patterns
- **Python**: Always use `.venv`. Run commands via `.venv/Scripts/python` (Windows) or `.venv/bin/python` (POSIX). Never use global Python or global `pip install`.
- **Node**: Use local `node_modules` and package scripts.
- **Flutter**: Use project-local Flutter SDK tooling and cached `.dart_tool`.
- **Database Isolation**: Tests must target isolated local test databases (e.g. SQLite test file or local test container) via `TEST_DATABASE_URL`. Never target production URLs.

## 4. Dual-Import Compatibility Pattern (Python)
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
