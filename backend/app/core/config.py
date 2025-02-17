from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://user:password@mysql/dbname"
    redis_url: str = "redis://redis:6379/0"
    LOG_LEVEL: str = "INFO"  # DEBUG, WARNING, ERROR
    ENVIRONMENT: str = "development"  #  production


settings = Settings()
