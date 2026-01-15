from pydantic import BaseSettings

class Settings(BaseSettings):
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1"
    LLM_TEMPERATURE: float = 0.1
    LLM_NUM_CTX: int = 8192

    class Config:
        env_file = ".env"

settings = Settings()
