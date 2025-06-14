"""
Basic Django setup tests to ensure everything is working.
"""

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.unit
@pytest.mark.django_db
class TestDjangoSetup:
    """Test that Django is properly configured."""

    def test_django_settings_configured(self):
        """Test that Django settings are properly configured."""
        assert settings.configured
        assert hasattr(settings, "DATABASES")
        assert hasattr(settings, "SECRET_KEY")

    def test_user_model_configured(self):
        """Test that the custom user model is configured."""
        assert User is not None
        assert hasattr(User, "email")
        assert hasattr(User, "objects")

    def test_database_connection(self):
        """Test that database connection works."""
        # This should not raise an error
        user_count = User.objects.count()
        assert isinstance(user_count, int)

    def test_user_creation_basic(self, user_factory):
        """Test basic user creation with factory."""
        user = user_factory()
        assert user.pk is not None
        assert user.email is not None
        assert "@" in user.email

    def test_factory_boy_working(self, user_factory):
        """Test that Factory Boy is working correctly."""
        users = user_factory.create_batch(3)
        assert len(users) == 3

        # All users should have unique emails
        emails = [user.email for user in users]
        assert len(set(emails)) == 3
