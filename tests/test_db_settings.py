import os
from unittest import mock

import pytest
from pydantic import ValidationError

from config.settings.databases import BaseDatabaseSettings, DBEngineEnum


class TestBaseDatabaseSettings:
    """Test suite for BaseDatabaseSettings class."""

    def test_model_dump_renders_enum_value_with_str(self):
        """Test that model_dump() renders DBEngineEnum
        value when initialized with string."""
        settings = BaseDatabaseSettings(engine="POSTGRES", name="some_db")

        dumped = settings.model_dump()
        assert dumped["engine"] == "django.db.backends.postgresql"
        assert dumped["engine"] != "POSTGRES"

    def test_model_dump_renders_enum_value_not_name(self):
        """Test that model_dump() renders DBEngineEnum value instead of name."""
        # Test with SQLITE engine
        settings = BaseDatabaseSettings(
            engine=DBEngineEnum.SQLITE, name="test_db.sqlite3"
        )

        dumped = settings.model_dump()

        # Should contain the enum value, not the name
        assert dumped["engine"] == "django.db.backends.sqlite3"
        assert dumped["engine"] != "SQLITE"

    def test_model_dump_with_postgres_engine(self):
        """Test model_dump() with PostgreSQL engine."""
        settings = BaseDatabaseSettings(
            engine=DBEngineEnum.POSTGRES, name="postgres_db"
        )

        dumped = settings.model_dump()

        assert dumped["engine"] == "django.db.backends.postgresql"
        assert dumped["engine"] != "POSTGRES"

    def test_enum_values_are_correct(self):
        """Test that all enum values are correct."""
        assert DBEngineEnum.SQLITE == "django.db.backends.sqlite3"
        assert DBEngineEnum.POSTGRES == "django.db.backends.postgresql"

    def test_settings_initialization_with_string_value(self):
        """Test that settings can be initialized with string values."""
        # Should work with string values that match enum values
        settings = BaseDatabaseSettings(
            engine="django.db.backends.sqlite3", name="test.db"
        )

        assert settings.engine == DBEngineEnum.SQLITE
        dumped = settings.model_dump()
        assert dumped["engine"] == "django.db.backends.sqlite3"

    def test_settings_initialization_with_enum(self):
        """Test that settings can be initialized with enum instances."""
        settings = BaseDatabaseSettings(
            engine=DBEngineEnum.POSTGRES, name="test_db"
        )

        assert settings.engine == DBEngineEnum.POSTGRES
        dumped = settings.model_dump()
        assert dumped["engine"] == "django.db.backends.postgresql"

    def test_model_dump_structure(self):
        """Test that model_dump() returns the expected structure."""
        settings = BaseDatabaseSettings(engine=DBEngineEnum.SQLITE)

        dumped = settings.model_dump()

        assert set(dumped.keys()) == {"engine"}

        # Check types
        assert isinstance(dumped["engine"], str)

    def test_model_dump_renders_enum_value_with_str_from_env(self):
        """Test that model_dump() renders DBEngineEnum value when engine comes
        from environment variable."""
        with mock.patch.dict(
            os.environ,
            {
                "DATABASE_ENGINE": "django.db.backends.postgresql",
                "DATABASE_NAME": "prod_db",
            },
        ):
            settings = BaseDatabaseSettings()

            dumped = settings.model_dump()

            # Should render the enum value
            assert dumped["engine"] == "django.db.backends.postgresql"

    def test_validation_error_shows_enum_names_and_values(self):
        """Test that validation error shows both enum names and values."""
        with pytest.raises(ValidationError) as exc_info:
            BaseDatabaseSettings(engine="INVALID", name="test")

        error_message = str(exc_info.value)

        # Should contain enum names
        assert "SQLITE" in error_message
        assert "POSTGRES" in error_message

        # Should contain enum values
        assert "django.db.backends.sqlite3" in error_message
        assert "django.db.backends.postgresql" in error_message
