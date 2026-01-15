# backend/config/llm_config.py

"""
Centralised LLM configuration for OpenRouter.

- Loads .env from:
    1) backend/.env      (BASE_DIR)
    2) project_root/.env (one level up)
- Exposes a single `llm_config` object.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


# -------- locate and load .env --------

BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
PROJECT_ROOT = BASE_DIR.parent                     # Scriptwise_Multiagent_Backend/

_loaded_env: str | None = None

for candidate in (BASE_DIR / ".env", PROJECT_ROOT / ".env"):
    if candidate.exists():
        load_dotenv(candidate)
        _loaded_env = str(candidate)
        break


# -------- Pydantic settings model --------

class LLMConfig(BaseSettings):
    openrouter_api_key: str = Field(..., env="OPENROUTER_API_KEY")
    model: str = Field("meta-llama/llama-3.1-70b-instruct", env="OPENROUTER_MODEL")
    base_url: str = Field("https://openrouter.ai/api/v1", env="OPENROUTER_BASE_URL")
    temperature: float = Field(0.2, env="LLM_TEMPERATURE")
    max_tokens: int = Field(1024, env="LLM_MAX_TOKENS")

    class Config:
        extra = "ignore"  # ignore unrelated env vars


# Single shared config instance
llm_config = LLMConfig()


# -------- optional debug CLI --------

if __name__ == "__main__":
    print(f"[LLM_CONFIG] BASE_DIR      = {BASE_DIR}")
    print(f"[LLM_CONFIG] PROJECT_ROOT  = {PROJECT_ROOT}")
    print(f"[LLM_CONFIG] CWD           = {Path.cwd()}")
    print(f"[LLM_CONFIG] Loaded .env   = {_loaded_env}")
    print(f"[LLM_CONFIG] API key present? {bool(llm_config.openrouter_api_key)}")
    print(
        f"[LLM_CONFIG] Using model={llm_config.model}, "
        f"base_url={llm_config.base_url}, "
        f"temp={llm_config.temperature}, "
        f"max_tokens={llm_config.max_tokens}"
    )
