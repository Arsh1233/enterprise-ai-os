# Enterprise AI Operating System (EAIOS) - Backend Foundation

This directory contains the FastAPI-based backend foundation for the EAIOS platform, prepared for subsequent AI, database, and infrastructure integration (Story 1.3).

## Architecture

The backend follows a flat `app/` architecture to avoid unnecessary depth while grouping concerns logically:
- **`app/api/`**: The FastAPI routers and endpoints for the API, organized by version.
- **`app/core/`**: Application factory, lifespan, and foundational bootstrapping.
- **`app/config/`**: Pydantic `BaseSettings` configurations loading from environment variables.
- **`app/logging/`**: Structured JSON logging setup via `structlog`.
- **`app/middleware/`**: Cross-cutting HTTP middlewares (Logging, Process time, CORS, Request ID, etc.).
- **`app/exceptions/`**: Centralized HTTP and Validation exception handling returning consistent `ORJSON` responses.

## Folder Structure

```text
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── health.py
│   │       ├── root.py
│   │       ├── version.py
│   │       └── router.py
│   ├── core/
│   ├── config/
│   ├── logging/
│   ├── middleware/
│   ├── exceptions/
│   ├── dependencies/
│   ├── schemas/
│   ├── services/
│   └── utils/
├── tests/
├── scripts/
├── main.py              # Application entrypoint
├── Makefile
├── pyproject.toml       # uv / PEP 621 Config
└── Dockerfile
```

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for lightning-fast dependency management instead of Poetry.

1. Install `uv`.
2. Clone the repository and navigate to the `backend/` directory.
3. Install dependencies:
```bash
make install
# or
uv pip install -e ".[dev]"
```

## Running

To start the local Uvicorn development server:
```bash
make run
# or
uvicorn main:app --reload
```
The server will run on `http://localhost:8000`. 
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Testing

Tests are written using `pytest`.
```bash
make test
```

## Formatting & Code Quality

This project enforces code quality through `black` (formatting), `ruff` (linting), and `mypy` (static type checking). 

To run linters:
```bash
make lint
```

To format code:
```bash
make format
```

To run type checks:
```bash
make typecheck
```

## Development Workflow

1. Configure `.env` in `backend/` by copying standard properties.
2. Ensure you have `pre-commit` hooks installed for continuous validation (`pre-commit install`).
3. Maintain type hints across all contributions.
4. No wildcard imports, global state, or duplicated code.
