from pydantic_settings import BaseSettings, SettingsConfigDict


class DbEngine(BaseSettings):
    """Manage Engine settings only"""

    ENGINE: str = "django.db.backends.sqlite3"
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )


class SQLiteSettings(DbEngine):
    """Manage sqlite settings only"""

    NAME: str = "db.sqlite3"


class PostgresSettings(BaseSettings):
    ENGINE: str = "django.db.backends.postgresql"
    NAME: str
    HOST: str
    PORT: str
    USER: str
    PASSWORD: str
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="POSTGRES_",
        case_sensitive=True,
    )


class DatabaseSettings(BaseSettings):
    """Manage databases settings"""

    default: SQLiteSettings | PostgresSettings

    @classmethod
    def get_db_settings(cls):
        engine: DbEngine = DbEngine()
        if "postgres" in engine.ENGINE:
            return cls(default=PostgresSettings())  # type: ignore
        return cls(default=SQLiteSettings())


class BaseEnv(BaseSettings):
    DEBUG: bool = True
    SECRET_KEY: str = (
        "django-insecure-!*f!8&^-h8oi0+)=r5rv0mifpem=@l18wr&3d!d06@be)@u53w"
    )
    ALLOWED_HOSTS: list[str] = ["*"]
    DATABASES: DatabaseSettings = DatabaseSettings.get_db_settings()
    STATIC_URL: str = "assets/"
    AUTH_USER_MODEL: str = "authentication.User"
    INTERNAL_IPS: tuple = ("127.0.0.1",)
    ROOT_URLCONF: str = "config.urls"
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )


class EnvironSettings(BaseEnv):
    pass


class LocalConfig(BaseSettings):
    ADDITIONAL_APPS: list[str] = [
    ]
