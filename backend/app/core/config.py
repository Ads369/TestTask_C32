from pydantic import HttpUrl
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

    @property
    def BASE_MYSQL_URL(self) -> str:
        return f"{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SQLALCHEMY_DATABASE_URL_ASYNC(self) -> str:
        # asyncmy не ставится на M1
        return f"mysql+aiomysql://{self.BASE_MYSQL_URL}"


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


class CBRFSettings(BaseSettings):
    EXTERNAL_API_TIMEOUT: int = 10
    EXTERNAL_API_MAX_RETRIES: int = 2
    USER_AGENT: str = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    CBR_API_URL: HttpUrl = HttpUrl("https://www.cbr-xml-daily.ru/")
    REDIS_DATA_KEY: str = "cbrf:daily_rates:data"
    REDIS_USD_KEY: str = "cbrf:daily_rates:usd"


class SesssionSetting(BaseSettings):
    SESSION_COOKIE_NAME: str = "session_id"
    SESSION_LIFETIME: int = 7 * 24 * 3600  # 7 дней
    SESSION_COOKIE_SECURE: bool = True
    SESSION_AUTO_CLEANUP: bool = True


class Settings(DatabaseSettings, RedisSettings, CBRFSettings, BaseSettings):
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"  # DEBUG, WARNING, ERROR
    ENVIRONMENT: str = "development"  #  production


settings = Settings()
