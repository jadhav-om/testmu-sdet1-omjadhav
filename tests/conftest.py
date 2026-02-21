from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

from src.llm.failure_explainer import generate_failure_explanation

REPORT_DIR = Path("reports")
LLM_DIR = REPORT_DIR / "llm"
LLM_RESULTS: list[dict[str, str]] = []


@pytest.fixture
def llm_context(request: pytest.FixtureRequest) -> dict[str, Any]:
    context: dict[str, Any] = {}
    setattr(request.node, "_llm_context", context)
    return context


def _safe_file_name(test_id: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", test_id)


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session: pytest.Session) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    LLM_DIR.mkdir(parents=True, exist_ok=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[Any]):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or report.passed:
        return

    extra_context: dict[str, Any] = {}
    node_ctx = getattr(item, "_llm_context", None)
    if isinstance(node_ctx, dict):
        extra_context.update(node_ctx)

    page = item.funcargs.get("page") if hasattr(item, "funcargs") else None
    if page is not None:
        try:
            extra_context["page_url"] = page.url
            extra_context["page_title"] = page.title()
            extra_context["dom_snippet"] = page.content()[:2000]
            screenshot_path = LLM_DIR / f"{_safe_file_name(item.nodeid)}.png"
            page.screenshot(path=str(screenshot_path), full_page=True)
            extra_context["screenshot"] = str(screenshot_path)
        except Exception as exc:  # pragma: no cover
            extra_context["ui_capture_error"] = str(exc)

    error_text = str(call.excinfo.value) if call.excinfo else "Unknown failure"
    explanation = generate_failure_explanation(
        test_name=item.nodeid,
        error=error_text,
        extra_context=extra_context,
    )

    output = {
        "test": item.nodeid,
        "explanation": explanation,
    }
    LLM_RESULTS.append(output)

    markdown_path = LLM_DIR / f"{_safe_file_name(item.nodeid)}.md"
    markdown_path.write_text(
        f"# LLM Failure Explanation\n\n"
        f"**Test**: `{item.nodeid}`\n\n"
        f"## Model Output\n\n{explanation}\n",
        encoding="utf-8",
    )

    jsonl_path = REPORT_DIR / "llm_failure_results.jsonl"
    with jsonl_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(output, ensure_ascii=True) + "\n")

    report.sections.append(("LLM Failure Explainer", explanation))


@pytest.hookimpl
def pytest_terminal_summary(terminalreporter: pytest.TerminalReporter) -> None:
    if not LLM_RESULTS:
        return

    terminalreporter.section("LLM Failure Explainer Summary", sep="=")
    for result in LLM_RESULTS:
        terminalreporter.write_line(f"Test: {result['test']}")
        terminalreporter.write_line(result["explanation"])
        terminalreporter.write_line("-" * 70)