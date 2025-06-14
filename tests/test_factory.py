import os
from unittest import mock

from config.settings.databases import BaseDatabaseSettings
from config.settings.factory import DbContainer


def test_db_factory():
    postgres = {
        "DATABASE_ENGINE": "django.db.backends.postgresql",
        "DATABASE_NAME": "prod_db",
        "DATABASE_USER": "prod_user",
        "DATABASE_PASSWORD": "prod_pass",
    }
    with mock.patch.dict(os.environ, postgres):
        dbcontainer = DbContainer()
        dbcontainer.config.from_pydantic(BaseDatabaseSettings())
        db = dbcontainer.django_databases().model_dump(
            mode="json", by_alias=True
        )
        assert db["default"]["ENGINE"] == "django.db.backends.postgresql"
        assert db["default"]["NAME"] == "prod_db"
