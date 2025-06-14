"""
Pytest configuration for API tests.
"""

import pytest
from django.urls import reverse

from modules.user.conftest import *  # noqa: F403


@pytest.fixture
def api_urls():
    """Provide common API URL patterns for tests."""
    return {
        "token_obtain": reverse("api:v1:user:token_obtain"),
        "token_refresh": reverse("api:v1:user:token_refresh"),
        "token_verify": reverse("api:v1:user:token_verify"),
    }


@pytest.fixture
def expected_user_fields():
    """Expected fields in user API responses."""
    return {
        "id",
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "date_of_birth",
        "is_active",
        "is_verified",
        "date_joined",
        "preferred_language",
        "timezone_preference",
        "display_name",
        "initials",
    }


@pytest.fixture
def login_data():
    """Valid login credentials for JWT authentication."""
    return {"email": "testuser@example.com", "password": "testpass123"}


@pytest.fixture
def invalid_login_data():
    """Invalid login credentials for testing authentication failures."""
    return {"email": "nonexistent@example.com", "password": "wrongpassword"}
