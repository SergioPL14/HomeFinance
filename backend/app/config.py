from pydantic_settings import BaseSettings
from functools import lru_cache
import yaml
from .utils.crypto import ConfigEncryption
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "HomefinanceApp"
    DATABASE_URL: str = "sqlite:///./financial_portfolio.db"
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Credenciales
    SANTANDER_USERNAME: str = ""
    SANTANDER_PASSWORD: str = ""
    SANTANDER_API_KEY: str = ""
    SANTANDER_API_SECRET: str = ""

    COINBASE_API_KEY: str = ""
    COINBASE_API_SECRET: str = ""

    @classmethod
    def from_yaml(cls, yaml_file: str, encrypted: bool = True) -> "Settings":
        if encrypted:
            crypto = ConfigEncryption()
            yaml_content = crypto.decrypt_file(yaml_file)
            config_data = yaml.safe_load(yaml_content)
        else:
            with open(yaml_file, 'r') as f:
                config_data = yaml.safe_load(f)

        # Extraer credenciales del YAML
        credentials = config_data.get('credentials', {})
        settings_data = config_data.get('settings', {})

        return cls(
            DATABASE_URL=settings_data.get('database_url'),
            JWT_SECRET_KEY=settings_data.get('jwt_secret'),
            
            # Santander credentials
            SANTANDER_USERNAME=credentials.get('santander', {}).get('username'),
            SANTANDER_PASSWORD=credentials.get('santander', {}).get('password'),
            SANTANDER_API_KEY=credentials.get('santander', {}).get('api_key'),
            SANTANDER_API_SECRET=credentials.get('santander', {}).get('api_secret'),
            
            # Coinbase credentials
            COINBASE_API_KEY=credentials.get('coinbase', {}).get('api_key'),
            COINBASE_API_SECRET=credentials.get('coinbase', {}).get('api_secret'),
        )

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    config_path = Path("config/config.yml.encrypted")
    if config_path.exists():
        return Settings.from_yaml(str(config_path))
    return Settings()

settings = get_settings()