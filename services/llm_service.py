from typing import Optional, List, Any
import os

from openai import OpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatResult, ChatGeneration

from config.llm_config import llm_config


class OpenRouterLLM(BaseChatModel):
    """Custom LangChain-compatible LLM wrapper for OpenRouter API."""
    
    client: Any = None
    model: str = ""
    temperature: float = 0.7
    max_tokens: int = 4096

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, client: OpenAI, model: str, temperature: float, max_tokens: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.client = client
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def _convert_messages(self, messages: List[BaseMessage]) -> List[dict]:
        """Convert LangChain messages to OpenAI format."""
        result = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                result.append({"role": "system", "content": msg.content})
            elif isinstance(msg, HumanMessage):
                result.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                result.append({"role": "assistant", "content": msg.content})
            else:
                result.append({"role": "user", "content": str(msg.content)})
        return result

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate a chat response from the OpenRouter API."""
        openai_messages = self._convert_messages(messages)
        
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=openai_messages,
            stop=stop,
        )
        
        content = response.choices[0].message.content or ""
        message = AIMessage(content=content)
        generation = ChatGeneration(message=message)
        
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "openrouter"


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
