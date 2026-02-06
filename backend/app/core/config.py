from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI-First CRM HCP"
    database_url: str = Field(default="sqlite:///./ai_first_crm.db", alias="DATABASE_URL")
    groq_api_key: str | None = Field(default=None, alias="GROQ_API_KEY")
    groq_model: str = Field(default="gemma2-9b-it", alias="GROQ_MODEL")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
