from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from src.config import settings
from src.llm.openai_client import OpenAIClient


PROMPT_TEMPLATE = """You are a senior SDET failure analysis assistant.
Analyze the failed test context and return a concise report with these exact headings:
1) What failed
2) Most likely root cause
3) Suggested fix
4) Confidence (High/Medium/Low)

Context:
{context}
"""


def _serialize_context(test_name: str, error: str, extra_context: dict[str, Any]) -> str:
    payload = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "test_name": test_name,
        "error": error,
        "extra_context": extra_context,
    }
    return json.dumps(payload, indent=2, ensure_ascii=True)


def generate_failure_explanation(
    test_name: str,
    error: str,
    extra_context: dict[str, Any],
) -> str:
    if not settings.enable_llm_failure_explainer:
        return "LLM Failure Explainer disabled via ENABLE_LLM_FAILURE_EXPLAINER=false"

    if not settings.openai_api_key:
        return "LLM Failure Explainer skipped: OPENAI_API_KEY not set"

    prompt = PROMPT_TEMPLATE.format(
        context=_serialize_context(test_name=test_name, error=error, extra_context=extra_context)
    )

    client = OpenAIClient(api_key=settings.openai_api_key, model=settings.openai_model)
    return client.explain_failure(prompt)