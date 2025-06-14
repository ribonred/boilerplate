import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class DefaultUserManager(BaseUserManager):
    """
    Default user manager that handles user creation with email
    as the unique identifier.
    """

    def _create_user(
        self, email: str, password: str, **extra_fields
    ) -> "AbstractUser":
        """Create and save a user with the given email and password."""
        if not email:
            raise ValueError(_("The Email field must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email: str, password: str | None = None, **extra_fields
    ) -> "AbstractUser":
        """Create and save a regular user with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str, password: str, **extra_fields
    ) -> "AbstractUser":
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    Abstract user model that provides a fully-featured user model with
    admin-compliant permissions and authentication.

    Email is used as the unique identifier instead of username.
    """

    # User identification fields
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("ID"),
    )

    email = models.EmailField(
        _("email address"),
        unique=True,
        max_length=254,
        help_text=_("Required. Enter a valid email address."),
    )

    # Personal information fields
    first_name = models.CharField(
        _("first name"),
        max_length=150,
        blank=True,
        help_text=_("Optional. 150 characters or fewer."),
    )

    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=True,
        help_text=_("Optional. 150 characters or fewer."),
    )

    # Phone number with validation
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message=_(
            'Phone number must be entered in the format: "+999999999". '
            "Up to 15 digits allowed."
        ),
    )
    phone_number = models.CharField(
        _("phone number"),
        validators=[phone_regex],
        max_length=17,
        blank=True,
        help_text=_("Optional. Phone number in international format."),
    )

    # Profile information
    date_of_birth = models.DateField(
        _("date of birth"),
        null=True,
        blank=True,
        help_text=_("Optional. Your date of birth."),
    )

    # Account status fields
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )

    is_verified = models.BooleanField(
        _("email verified"),
        default=False,
        help_text=_(
            "Designates whether the user has verified their email address."
        ),
    )

    # Timestamp fields
    date_joined = models.DateTimeField(
        _("date joined"),
        default=timezone.now,
        help_text=_("The date and time when the user account was created."),
    )

    last_login = models.DateTimeField(
        _("last login"),
        blank=True,
        null=True,
        help_text=_("The date and time of the user's last login."),
    )

    email_verified_at = models.DateTimeField(
        _("email verified at"),
        null=True,
        blank=True,
        help_text=_("The date and time when the email was verified."),
    )

    # Preference fields
    preferred_language = models.CharField(
        _("preferred language"),
        max_length=10,
        choices=[
            ("en", _("English")),
            ("id", _("Indonesian")),
        ],
        default="en",
        help_text=_("User's preferred language for the interface."),
    )

    timezone_preference = models.CharField(
        _("timezone"),
        max_length=50,
        default="UTC",
        help_text=_("User's preferred timezone."),
    )

    # Marketing preferences
    email_notifications = models.BooleanField(
        _("email notifications"),
        default=True,
        help_text=_("Receive email notifications for important updates."),
    )

    marketing_emails = models.BooleanField(
        _("marketing emails"),
        default=False,
        help_text=_("Receive marketing and promotional emails."),
    )

    # Security fields
    password_changed_at = models.DateTimeField(
        _("password changed at"),
        null=True,
        blank=True,
        help_text=_("The date and time when the password was last changed."),
    )

    failed_login_attempts = models.PositiveIntegerField(
        _("failed login attempts"),
        default=0,
        help_text=_("Number of consecutive failed login attempts."),
    )

    account_locked_until = models.DateTimeField(
        _("account locked until"),
        null=True,
        blank=True,
        help_text=_("Account is locked until this date and time."),
    )

    objects = DefaultUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        abstract = True
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["is_active", "is_staff"]),
            models.Index(fields=["date_joined"]),
            models.Index(fields=["last_login"]),
        ]

    def __str__(self) -> str:
        """Return the string representation of the user."""
        return self.email

    def __repr__(self) -> str:
        """Return the detailed string representation of the user."""
        return f"<{self.__class__.__name__}: {self.email}>"

    def clean(self) -> None:
        """Perform model validation."""
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self) -> str:
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.email

    def get_short_name(self) -> str:
        """Return the short name for the user."""
        return self.first_name or self.email.split("@")[0]

    def email_user(
        self,
        subject: str,
        message: str,
        from_email: str | None = None,
        **kwargs,
    ) -> None:
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def verify_email(self) -> None:
        """Mark the user's email as verified."""
        self.is_verified = True
        self.email_verified_at = timezone.now()
        self.save(update_fields=["is_verified", "email_verified_at"])

    def is_account_locked(self) -> bool:
        """Check if the account is currently locked."""
        if self.account_locked_until:
            return timezone.now() < self.account_locked_until
        return False

    def lock_account(self, duration_minutes: int = 30) -> None:
        """Lock the account for the specified duration."""
        self.account_locked_until = timezone.now() + timezone.timedelta(
            minutes=duration_minutes
        )
        self.save(update_fields=["account_locked_until"])

    def unlock_account(self) -> None:
        """Unlock the account and reset failed login attempts."""
        self.account_locked_until = None
        self.failed_login_attempts = 0
        self.save(
            update_fields=["account_locked_until", "failed_login_attempts"]
        )

    def increment_failed_login(self) -> None:
        """
        Increment failed login attempts and lock account if threshold reached.
        """
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:  # Lock after 5 failed attempts
            self.lock_account()
        self.save(update_fields=["failed_login_attempts"])

    def reset_failed_login(self) -> None:
        """Reset failed login attempts counter."""
        self.failed_login_attempts = 0
        self.save(update_fields=["failed_login_attempts"])

    def set_password(self, raw_password: str) -> None:
        """Set the user's password and update password_changed_at."""
        super().set_password(raw_password)
        self.password_changed_at = timezone.now()

    def get_age(self) -> int | None:
        """Calculate and return the user's age based on date_of_birth."""
        if self.date_of_birth:
            today = timezone.now().date()
            return (
                today.year
                - self.date_of_birth.year
                - (
                    (today.month, today.day)
                    < (self.date_of_birth.month, self.date_of_birth.day)
                )
            )
        return None

    def is_birthday_today(self) -> bool:
        """Check if today is the user's birthday."""
        if self.date_of_birth:
            today = timezone.now().date()
            return (today.month, today.day) == (
                self.date_of_birth.month,
                self.date_of_birth.day,
            )
        return False

    @property
    def display_name(self) -> str:
        """Return the best available name for display purposes."""
        return self.get_full_name()

    @property
    def initials(self) -> str:
        """Return the user's initials."""
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        elif self.first_name:
            return self.first_name[0].upper()
        else:
            return self.email[0].upper()


class User(AbstractUser):
    """
    Concrete user model that inherits from AbstractUser.
    This is the actual user model that will be used in the application.
    """

    class Meta(AbstractUser.Meta):
        abstract = False
        db_table = "auth_user"
        swappable = "AUTH_USER_MODEL"
