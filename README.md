# Hybrid Test Automation Portfolio

[![CI](https://github.com/maderkabest/automation-portfolio-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/maderkabest/automation-portfolio-demo/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-latest-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/python/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Docker](https://img.shields.io/badge/Docker-PostgreSQL-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

## What This Project Demonstrates

This framework solves a real-world testing problem: **UI-only E2E tests are slow, flaky, and hard to scale**. Instead, this project practically applies the Testing Pyramid — using the right layer for the right job to maximize speed and reliability.

- **API layer** validates core business logic instantly, bypassing the browser entirely
- **UI layer** focuses strictly on what requires a real browser
- **Hybrid layer** combines both: API for setup, UI for user actions — saving 10-15s per test
- **Integration layer** verifies data persistence directly in PostgreSQL
- **CI pipeline** runs all layers in parallel with Cloudflare-aware graceful degradation

## Test Architecture

| Layer | Directory | What It Demonstrates |
|-------|-----------|----------------------|
| API | `tests/api/` | REST API testing, Pydantic validation, auth flows |
| UI | `tests/ui/` | Page Object Model, Playwright locators, Angular SPA |
| Hybrid | `tests/hybrid/` | API preconditions + UI actions, Magic Login via localStorage |
| Integration | `tests/integration/` | Direct DB access via psycopg2, data persistence verification |

## How to Run

**Prerequisites:** Python 3.12+, Docker Desktop

```bash
# 1. Clone and install
git clone https://github.com/maderkabest/automation-portfolio-demo.git
cd automation-portfolio-demo
pip install -r requirements.txt
playwright install chromium

# 2. Configure environment
cp .env.example .env
# Edit .env with your values

# 3. Run API tests (no Docker needed)
pytest tests/api/ -v

# 4. Start Docker and run integration tests
docker compose -f docker/docker-compose.yml --env-file .env up -d
pytest tests/integration/ -v

# 5. Run UI and Hybrid tests
pytest tests/ui/ tests/hybrid/ -v
```

## ⚠️ Known Limitations (CI/CD)

The UI and Hybrid test suites (`tests/ui/`, `tests/hybrid/`) run perfectly on local machines. However, in the GitHub Actions environment, the target website (`practicesoftwaretesting.com`) actively blocks requests from GitHub's datacenter IP addresses using Cloudflare WAF (returning `HTTP 403 + cf-mitigated: challenge`).

**How this is handled in this project:**

- The CI pipeline includes a pre-check step that detects Cloudflare blocking
- If a block is detected, the pipeline gracefully skips UI test execution
- A summary message is posted to the Workflow Summary explaining the limitation
- API and Integration tests continue to run and pass normally

To run the full E2E suite, execute the tests locally following the setup instructions above.

## Playwright Trace Viewer

UI and Hybrid test runs generate a full execution trace with screenshots, DOM snapshots, and network activity — useful for debugging failures without re-running tests.

```bash
playwright show-trace test-results/trace.zip
```

![Playwright Trace Viewer](docs/trace-viewer.png)
