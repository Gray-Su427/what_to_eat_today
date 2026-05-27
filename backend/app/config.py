from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://eat:eat@localhost:5432/eat"
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24小时

    class Config:
        env_file = ".env"


settings = Settings()
