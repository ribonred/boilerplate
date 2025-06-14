"""
Pytest configuration and fixtures for user module tests.
"""

import factory
import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker

fake = Faker()
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating User instances
    using the proper create_user method."""

    class Meta:
        model = User
        django_get_or_create = ("email",)

    # Core fields
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    # Phone number with proper format
    phone_number = factory.Faker("phone_number")

    # Personal information
    date_of_birth = factory.Faker(
        "date_of_birth", minimum_age=18, maximum_age=80
    )

    # Account status
    is_active = True
    is_staff = False
    is_superuser = False
    is_verified = False  # Preferences
    preferred_language = "en"
    timezone_preference = "UTC"
    email_notifications = True
    marketing_emails = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override to use create_user method for proper email normalization."""
        # Extract email and password from kwargs
        email = kwargs.pop("email")
        password = kwargs.pop("password", "testpass123")

        # Use the manager's create_user method
        user = model_class.objects.create_user(
            email=email, password=password, **kwargs
        )
        return user


class VerifiedUserFactory(UserFactory):
    """Factory for creating verified users."""

    is_verified = True
    email_verified_at = factory.LazyFunction(timezone.now)


class StaffUserFactory(UserFactory):
    """Factory for creating staff users."""

    is_staff = True
    is_verified = True
    email_verified_at = factory.LazyFunction(timezone.now)


class AdminUserFactory(UserFactory):
    """Factory for creating admin users."""

    email = factory.Sequence(lambda n: f"admin{n}@example.com")
    is_staff = True
    is_superuser = True
    is_verified = True
    email_verified_at = factory.LazyFunction(timezone.now)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override to use create_superuser method."""
        # Extract email and password from kwargs
        email = kwargs.pop("email")
        password = kwargs.pop("password", "testpass123")

        # Use the manager's create_superuser method
        user = model_class.objects.create_superuser(
            email=email, password=password, **kwargs
        )
        return user


class InactiveUserFactory(UserFactory):
    """Factory for creating inactive users."""

    is_active = False


class LockedUserFactory(UserFactory):
    """Factory for creating locked users."""

    failed_login_attempts = 5
    account_locked_until = factory.LazyFunction(
        lambda: timezone.now() + timezone.timedelta(minutes=30)
    )


# Pytest fixtures
@pytest.fixture
def user_factory():
    """Provide the UserFactory for tests."""
    return UserFactory


@pytest.fixture
def verified_user_factory():
    """Provide the VerifiedUserFactory for tests."""
    return VerifiedUserFactory


@pytest.fixture
def staff_user_factory():
    """Provide the StaffUserFactory for tests."""
    return StaffUserFactory


@pytest.fixture
def admin_user_factory():
    """Provide the AdminUserFactory for tests."""
    return AdminUserFactory


@pytest.fixture
def inactive_user_factory():
    """Provide the InactiveUserFactory for tests."""
    return InactiveUserFactory


@pytest.fixture
def locked_user_factory():
    """Provide the LockedUserFactory for tests."""
    return LockedUserFactory


@pytest.fixture
def user(user_factory):
    """Create a single user instance for tests."""
    return user_factory()


@pytest.fixture
def verified_user(verified_user_factory):
    """Create a verified user instance for tests."""
    return verified_user_factory()


@pytest.fixture
def staff_user(staff_user_factory):
    """Create a staff user instance for tests."""
    return staff_user_factory()


@pytest.fixture
def admin_user(admin_user_factory):
    """Create an admin user instance for tests."""
    return admin_user_factory()


@pytest.fixture
def users(user_factory):
    """Create multiple user instances for tests."""
    return user_factory.create_batch(5)


@pytest.fixture
def user_data():
    """Provide valid user data for tests."""
    return {
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "phone_number": "+1234567890",
        "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=80),
        "preferred_language": "en",
        "timezone_preference": "UTC",
        "password": "testpass123",
    }


@pytest.fixture
def invalid_user_data():
    """Provide invalid user data for tests."""
    return {
        "email": "invalid-email",
        "first_name": "",
        "last_name": "",
        "phone_number": "invalid-phone",
        "date_of_birth": "2030-01-01",  # Future date
        "preferred_language": "invalid",
        "password": "123",  # Too short
    }
