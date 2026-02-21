# TestMu SDET-1 Hackathon Assignment Submission

This repository contains a complete SDET-1 assignment implementation using **Python + pytest + Playwright** with a real **LLM API integration** (Task 3, Option A).

## Assignment Mapping

- Task 1 (Setup & Scaffold): Project structure and runnable automation framework are included.
- Task 2 (Prompt Engineering): `prompts.md` + generated module test cases in `generated-test-cases/`.
- Task 3 (LLM Integration): Real OpenAI API call on failures via `tests/conftest.py` + `src/llm/`.

## Why Option A (Failure Explainer)

Option A provides direct debugging acceleration during active test development by attaching root-cause hypotheses and suggested fixes exactly when a test fails. This reduces triage time in day-to-day regression execution more immediately than post-run flaky classification.

## Tech Stack

- Python 3.11+
- pytest
- Playwright (UI)
- requests + jsonschema (API)
- OpenAI API (`openai` SDK)

## Project Structure

```text
.
|-- ai-usage-log.md
|-- prompts.md
|-- generated-test-cases/
|   |-- login_test_cases.feature
|   |-- dashboard_test_cases.feature
|   |-- api_test_cases.feature
|   |-- module_refinement_notes.md
|-- src/
|   |-- config.py
|   |-- llm/
|       |-- openai_client.py
|       |-- failure_explainer.py
|-- tests/
|   |-- conftest.py
|   |-- ui/
|   |   |-- test_login.py
|   |   |-- test_dashboard.py
|   |-- api/
|       |-- test_api.py
|-- reports/
|-- sample-output/
|   |-- llm_failure_response.md
|-- requirements.txt
|-- pytest.ini
|-- .env.example
```

## Step-by-Step Setup and Run

1. Create and activate virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```powershell
pip install -r requirements.txt
playwright install
```

3. Configure environment variables.

```powershell
Copy-Item .env.example .env
```

4. Edit `.env` and set your OpenAI key.

```env
OPENAI_API_KEY=<your-real-key>
OPENAI_MODEL=gpt-4.1-mini
ENABLE_LLM_FAILURE_EXPLAINER=true
```

5. Run full suite.

```powershell
pytest
```

6. Run only smoke tests.

```powershell
pytest -m smoke
```

7. Run module-specific suites.

```powershell
pytest tests/ui/test_login.py
pytest tests/ui/test_dashboard.py
pytest tests/api/test_api.py
```

## How LLM Integration Works (Task 3)

- Hook: `pytest_runtest_makereport` in `tests/conftest.py`.
- Trigger: Executes only when a test fails.
- Input to LLM: Test name, error details, page/API context.
- Output destinations:
  - `reports/llm/<test>.md`
  - `reports/llm_failure_results.jsonl`
  - Terminal summary section at end of pytest run.

This is a **real API call**, not a mock. If `OPENAI_API_KEY` is missing, the framework records a skip message.

## Notes About Target Systems Used in Demo

- UI module coverage uses `https://www.saucedemo.com` and forgot-password flow sample at `https://the-internet.herokuapp.com/forgot_password`.
- API module coverage uses `https://dummyjson.com`, `https://jsonplaceholder.typicode.com`, `https://api.github.com`, and `https://httpbin.org`.

## What I Would Build Next With More Time

1. Add Page Object Model + centralized selectors for maintainability.
2. Add CI pipeline (GitHub Actions) with scheduled regression and artifact uploads.
3. Add richer LLM output schema (JSON) and automatic Jira ticket draft generation from failures.
4. Expand API coverage with contract testing against versioned OpenAPI specs.
5. Add flaky-test quarantine strategy and reliability scoring dashboard.