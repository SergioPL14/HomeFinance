from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "HomefinanceApp"
    DATABASE_URL: str = "sqlite:///./financial_portfolio.db"
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # URLs de APIs (ejemplos)
    SANTANDER_API_URL: str = "https://api.santander.example"
    EVO_API_URL: str = "https://api.evo.example"
    REVOLUT_API_URL: str = "https://api.revolut.example"
    COINBASE_API_URL: str = "https://api.coinbase.com/v2"
    FINIZENS_API_URL: str = "https://api.finizens.example"
    INDEXA_API_URL: str = "https://api.indexacapital.example"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = Settings() 