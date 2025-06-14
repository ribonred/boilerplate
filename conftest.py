"""
Global pytest configuration for the mschool project.
"""

import pytest


@pytest.fixture(scope="session")
def django_db_setup():
    """
    Avoid creating/setting up the test database for tests that don't need it.
    """
    # settings.DATABASES["default"] = {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": ":memory:",
    #     "ATOMIC_REQUESTS": False,
    #     "AUTOCOMMIT": True,
    #     "CONN_MAX_AGE": 0,
    #     "OPTIONS": {},
    #     "TIME_ZONE": None,
    #     "USER": "",
    #     "PASSWORD": "",
    #     "HOST": "",
    #     "PORT": "",
    # }
    ...


@pytest.fixture
def api_client():
    """Provide a Django REST Framework API client."""
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client):
    """Provide an authenticated API client with a test user."""
    from modules.user.conftest import UserFactory

    user = UserFactory()
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def admin_api_client(api_client):
    """Provide an authenticated API client with an admin user."""
    from modules.user.conftest import AdminUserFactory

    admin_user = AdminUserFactory()
    api_client.force_authenticate(user=admin_user)
    return api_client, admin_user
