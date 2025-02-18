from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    DB_HOST: str = "mysql"
    DB_PORT: int = 3306
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "testdb"
    DB_POOL_SIZE: int = 5
    DB_POOL_RECYCLE: int = 300
    DB_ECHO: bool = False
    DB_MAX_OVERFLOW: int = 10


class RedisSettings(BaseSettings):
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    REDIS_SSL: bool = False
    REDIS_TIMEOUT: int = 10
    REDIS_POOL_SIZE: int = 10
    REDIS_RETRY_ON_TIMEOUT: bool = True
    CACHE_TTL: int = 300  # 5 minutes

    @property
    def REDIS_URL(self) -> str:
        scheme = "rediss" if self.REDIS_SSL else "redis"
        auth = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"{scheme}://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


class Settings(DatabaseSettings, RedisSettings, BaseSettings):
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"  # DEBUG, WARNING, ERROR
    ENVIRONMENT: str = "development"  #  production


settings = Settings()
