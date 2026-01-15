from typing import Optional
import os

from openai import OpenAI
from config.llm_config import llm_config


class OpenRouterLLM:
    def __init__(self, client: OpenAI, model: str, temperature: float, max_tokens: int) -> None:
        self.client = client
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def invoke(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content


_llm: Optional[OpenRouterLLM] = None


def get_llm() -> OpenRouterLLM:
    global _llm
    if _llm is not None:
        return _llm

    headers = {}
    http_referer = os.getenv("OPENROUTER_HTTP_REFERER")
    title = os.getenv("OPENROUTER_X_TITLE")
    if http_referer:
        headers["HTTP-Referer"] = http_referer
    if title:
        headers["X-Title"] = title

    client = OpenAI(
        base_url=llm_config.base_url,
        api_key=llm_config.openrouter_api_key,
        default_headers=headers or None,
    )

    _llm = OpenRouterLLM(
        client=client,
        model=llm_config.model,
        temperature=llm_config.temperature,
        max_tokens=llm_config.max_tokens,
    )
    return _llm
