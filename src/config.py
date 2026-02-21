from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    enable_llm_failure_explainer: bool = os.getenv(
        "ENABLE_LLM_FAILURE_EXPLAINER", "true"
    ).lower() in {"1", "true", "yes", "on"}


settings = Settings()