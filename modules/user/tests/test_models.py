"""
Unit tests for User model.
"""

from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils import timezone

User = get_user_model()


@pytest.mark.unit
@pytest.mark.user
@pytest.mark.django_db
class TestUserModel:
    """Test cases for User model functionality."""

    def test_user_creation_with_factory(self, user_factory):
        """Test user creation using factory."""
        user = user_factory()

        assert user.id is not None
        assert user.email is not None
        assert "@" in user.email
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_user_string_representation(self, user_factory):
        """Test user string representation."""
        user = user_factory(email="test@example.com")
        assert str(user) == "test@example.com"

    def test_user_repr(self, user_factory):
        """Test user repr representation."""
        user = user_factory(email="test@example.com")
        assert "test@example.com" in repr(user)
        assert "User" in repr(user)

    def test_user_get_full_name(self, user_factory):
        """Test get_full_name method."""
        user = user_factory(first_name="John", last_name="Doe")
        assert user.get_full_name() == "John Doe"

        # Test with only first name
        user_first_only = user_factory(first_name="John", last_name="")
        assert user_first_only.get_full_name() == "John"

        # Test with no names
        user_no_names = user_factory(first_name="", last_name="")
        assert user_no_names.get_full_name() == user_no_names.email

    def test_user_get_short_name(self, user_factory):
        """Test get_short_name method."""
        user = user_factory(first_name="John", email="john@example.com")
        assert user.get_short_name() == "John"

        # Test with no first name
        user_no_first = user_factory(first_name="", email="johnbig@example.com")
        assert user_no_first.get_short_name() == "johnbig"

    def test_user_display_name_property(self, user_factory):
        """Test display_name property."""
        user = user_factory(first_name="John", last_name="Doe")
        assert user.display_name == "John Doe"

    def test_user_initials_property(self, user_factory):
        """Test initials property."""
        user = user_factory(first_name="John", last_name="Doe")
        assert user.initials == "JD"

        # Test with only first name
        user_first_only = user_factory(
            first_name="John", last_name="", email="john@example.com"
        )
        assert user_first_only.initials == "J"

        # Test with no names
        user_no_names = user_factory(
            first_name="", last_name="", email="jane@example.com"
        )
        assert user_no_names.initials == "J"

    def test_email_normalization(self, user_factory):
        """Test email normalization."""
        user = user_factory(email="Test@EXAMPLE.COM")
        assert user.email == "Test@example.com"  # Domain should be lowercase

    def test_email_uniqueness(self, user_factory):
        """Test that emails must be unique."""
        _user1 = user_factory(email="test@example.com")

        with pytest.raises(IntegrityError):
            user_factory(email="test@example.com")

    def test_password_setting(self, user_factory):
        """Test password setting and verification."""
        user = user_factory()
        raw_password = "testpassword123"
        user.set_password(raw_password)

        assert user.check_password(raw_password)
        assert user.password_changed_at is not None
        assert user.password != raw_password  # Should be hashed

    def test_email_verification(self, user_factory):
        """Test email verification functionality."""
        user = user_factory(is_verified=False)
        assert not user.is_verified
        assert user.email_verified_at is None

        user.verify_email()
        assert user.is_verified
        assert user.email_verified_at is not None

    def test_account_locking(self, user_factory):
        """Test account locking functionality."""
        user = user_factory()
        assert not user.is_account_locked()

        user.lock_account(30)  # Lock for 30 minutes
        assert user.is_account_locked()
        assert user.account_locked_until is not None

        user.unlock_account()
        assert not user.is_account_locked()
        assert user.account_locked_until is None
        assert user.failed_login_attempts == 0

    def test_failed_login_attempts(self, user_factory):
        """Test failed login attempt tracking."""
        user = user_factory()
        assert user.failed_login_attempts == 0

        # Increment failed attempts
        for i in range(4):
            user.increment_failed_login()
            assert user.failed_login_attempts == i + 1
            assert not user.is_account_locked()

        # 5th attempt should lock the account
        user.increment_failed_login()
        assert user.failed_login_attempts == 5
        assert user.is_account_locked()

        # Reset should clear attempts
        user.reset_failed_login()
        assert user.failed_login_attempts == 0

    def test_age_calculation(self, user_factory):
        """Test age calculation."""
        # User born 25 years ago
        birth_date = date.today() - timedelta(days=25 * 365)
        user = user_factory(date_of_birth=birth_date)

        age = user.get_age()
        assert age in [24, 25]  # Could be 24 or 25 depending on exact date

        # User with no birth date
        user_no_birth = user_factory(date_of_birth=None)
        assert user_no_birth.get_age() is None

    def test_birthday_check(self, user_factory):
        """Test birthday checking."""
        # User with birthday today
        user_birthday_today = user_factory(date_of_birth=timezone.now())
        assert user_birthday_today.is_birthday_today()

        # User with birthday not today
        user_birthday_tomorrow = user_factory(
            date_of_birth=(date.today() + timedelta(days=1))
        )
        assert not user_birthday_tomorrow.is_birthday_today()

        # User with no birth date
        user_no_birth = user_factory(date_of_birth=None)
        assert not user_no_birth.is_birthday_today()


@pytest.mark.unit
@pytest.mark.user
@pytest.mark.django_db
class TestUserManager:
    """Test cases for User manager methods."""

    def test_create_user(self):
        """Test creating a regular user."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

        assert user.email == "test@example.com"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser
        assert user.check_password("testpass123")

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            email="admin@example.com", password="adminpass123"
        )

        assert user.email == "admin@example.com"
        assert user.is_active
        assert user.is_staff
        assert user.is_superuser
        assert user.check_password("adminpass123")

    def test_create_user_without_email(self):
        """Test that creating user without email raises error."""
        with pytest.raises(ValueError, match="The Email field must be set"):
            User.objects.create_user(email="", password="testpass123")

    def test_create_superuser_without_staff_flag(self):
        """Test that creating superuser without is_staff=True raises error."""
        with pytest.raises(
            ValueError, match="Superuser must have is_staff=True"
        ):
            User.objects.create_superuser(
                email="admin@example.com",
                password="adminpass123",
                is_staff=False,
            )

    def test_create_superuser_without_superuser_flag(self):
        """Test that creating superuser without i
        s_superuser=True raises error."""
        with pytest.raises(
            ValueError, match="Superuser must have is_superuser=True"
        ):
            User.objects.create_superuser(
                email="admin@example.com",
                password="adminpass123",
                is_superuser=False,
            )


@pytest.mark.unit
@pytest.mark.user
@pytest.mark.django_db
class TestUserFactories:
    """Test the user factories themselves."""

    def test_verified_user_factory(self, verified_user_factory):
        """Test verified user factory."""
        user = verified_user_factory()
        assert user.is_verified
        assert user.email_verified_at is not None

    def test_staff_user_factory(self, staff_user_factory):
        """Test staff user factory."""
        user = staff_user_factory()
        assert user.is_staff
        assert user.is_verified
        assert user.email_verified_at is not None

    def test_admin_user_factory(self, admin_user_factory):
        """Test admin user factory."""
        user = admin_user_factory()
        assert user.is_staff
        assert user.is_superuser
        assert user.is_verified
        assert user.email_verified_at is not None
        assert "admin" in user.email

    def test_inactive_user_factory(self, inactive_user_factory):
        """Test inactive user factory."""
        user = inactive_user_factory()
        assert not user.is_active

    def test_locked_user_factory(self, locked_user_factory):
        """Test locked user factory."""
        user = locked_user_factory()
        assert user.failed_login_attempts == 5
        assert user.account_locked_until is not None
        assert user.is_account_locked()

    def test_user_factory_with_password(self, user_factory):
        """Test user factory with custom password."""
        custom_password = "mycustompassword123"
        user = user_factory(password=custom_password)
        assert user.check_password(custom_password)

    def test_user_factory_batch_creation(self, user_factory):
        """Test creating multiple users with factory."""
        users = user_factory.create_batch(5)
        assert len(users) == 5

        # Check that all users have unique emails
        emails = [user.email for user in users]
        assert len(set(emails)) == 5  # All emails should be unique
