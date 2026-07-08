# Enterprise AI Operating System (EAIOS) - Backend Foundation

This directory contains the FastAPI-based backend foundation for the EAIOS platform.

## Architecture

The backend follows a flat `app/` architecture:
- **`app/api/`**: The FastAPI routers and endpoints for the API, organized by version.
- **`app/core/`**: Application factory, lifespan, and foundational bootstrapping.
- **`app/config/`**: Pydantic `BaseSettings` configurations loading from environment variables.
- **`app/logging/`**: Structured JSON logging setup via `structlog`.
- **`app/middleware/`**: Cross-cutting HTTP middlewares.
- **`app/exceptions/`**: Centralized HTTP and Validation exception handling.

## Developer Setup

1. Install [uv](https://github.com/astral-sh/uv).
2. Clone the repository and navigate to the `backend/` directory.
3. Install dependencies:
```bash
make install
# or
uv pip install -e ".[dev]"
```
4. Install `pre-commit` hooks:
```bash
pre-commit install
```

## Running

To start the local Uvicorn development server:
```bash
make run
# or
uvicorn app.main:app --reload
```

## Quality Commands

We maintain strict code quality standards enforced via Makefile targets:

- `make lint` - Runs Ruff to check for linting errors.
- `make format` - Runs Ruff to format the code automatically.
- `make typecheck` - Runs MyPy for static type checking.
- `make test` - Runs the test suite using Pytest.
- `make coverage` - Runs tests and generates a coverage report.
- `make ci` - Runs the full suite of checks performed in CI.

## CI

We use GitHub Actions for Continuous Integration. The CI pipeline runs on every `push` and `pull_request` to the `main` branch. It ensures that:
- Dependencies are successfully installed via `uv`.
- The code passes `ruff check` and `ruff format --check`.
- Static typing passes via `mypy`.
- The test suite passes and meets the coverage requirement.

## Coverage

Test coverage is enforced using `pytest-cov`.
- Target coverage: **80%+**
- Run locally with: `make coverage`
- Generates `coverage.xml` and terminal reports.
- Ignores `tests/` and `migrations/`.

## Contribution Workflow

1. Create a new branch for your feature or bugfix.
2. Make your changes in the `app/` directory.
3. Ensure you have run `make format` and `make lint`.
4. Verify your changes don't break typing by running `make typecheck`.
5. Write tests and ensure coverage remains above 80% with `make coverage`.
6. Commit your changes (pre-commit hooks will automatically run).
7. Submit a Pull Request and ensure the GitHub Actions CI pipeline passes.
