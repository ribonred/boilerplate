from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings):
    """Common settings for the application."""

    model_config = SettingsConfigDict(
        env_prefix="COMMON_",
        extra="ignore",
        frozen=True,
        alias_generator=lambda field_name: field_name.upper(),
        populate_by_name=True,
        env_file=".env",
    )

    # Add common settings here
    DEBUG: bool = False
    SECRET_KEY: str = "django-insecure-w_h*3y=%=5i-ns)u%@leujvxrm02exc=v*sob(!tt-=^1h=+4q"  # noqa: E501
    ALLOWED_HOSTS: list[str] = ["*"]
