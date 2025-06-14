from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.forms import CharField, ModelForm, PasswordInput
from django.utils.translation import gettext_lazy as _

from .models import User


class UserCreationForm(ModelForm):
    """
    A form that creates a user, with no privileges,
    from the given email and password.
    """

    password1 = CharField(
        label=_("Password"),
        widget=PasswordInput,
        help_text=_(
            "Your password can't be too similar to your other personal "
            "information. Your password must contain at least 8 characters. "
            "Your password can't be a commonly used password. "
            "Your password can't be entirely numeric."
        ),
    )
    password2 = CharField(
        label=_("Password confirmation"),
        widget=PasswordInput,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "date_of_birth",
        )

    def clean_password2(self):
        """Validate that the two password entries match."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords don't match"))
        return password2

    def clean_email(self):
        """Validate that the email is unique."""
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise ValidationError(_("A user with this email already exists."))
        return email

    def save(self, commit=True):
        """Save the provided password in hashed format."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(ModelForm):
    """
    A form for updating users. Includes all the fields on the user,
    but replaces the password field with admin's disabled password
    hash display field.
    """

    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            '<a href="{}">this form</a>.',
        ),
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "date_of_birth",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_verified",
            "preferred_language",
            "timezone_preference",
            "email_notifications",
            "marketing_emails",
            "groups",
            "user_permissions",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format(
                f"../../{self.instance.pk}/password/"
            )

    def clean_password(self):
        """
        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value.
        """
        return self.initial.get("password")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for the User model."""

    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_verified",
        "date_joined",
        "last_login",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "is_verified",
        "date_joined",
        "last_login",
        "preferred_language",
        "email_notifications",
        "marketing_emails",
    )

    search_fields = ("email", "first_name", "last_name", "phone_number")

    ordering = ("-date_joined",)

    filter_horizontal = ("groups", "user_permissions")

    readonly_fields = (
        "id",
        "date_joined",
        "last_login",
        "email_verified_at",
        "password_changed_at",
        "failed_login_attempts",
        "account_locked_until",
    )

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "date_of_birth",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Preferences"),
            {
                "fields": (
                    "preferred_language",
                    "timezone_preference",
                    "email_notifications",
                    "marketing_emails",
                ),
            },
        ),
        (
            _("Security"),
            {
                "fields": (
                    "password_changed_at",
                    "failed_login_attempts",
                    "account_locked_until",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Important dates"),
            {
                "fields": ("date_joined", "last_login", "email_verified_at"),
                "classes": ("collapse",),
            },
        ),
        (_("System"), {"fields": ("id",), "classes": ("collapse",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "date_of_birth",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        """Make ID field readonly for existing objects."""
        if obj:  # Editing an existing object
            return self.readonly_fields
        return ("id",)  # Creating a new object

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation.
        """
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def save_model(self, request, obj, form, change):
        """Override save_model to handle password changes."""
        if not change and hasattr(form, "save"):
            # This is a new user creation
            form.save()
        else:
            # This is an update
            super().save_model(request, obj, form, change)

    actions = [
        "make_active",
        "make_inactive",
        "verify_emails",
        "send_welcome_email",
    ]

    @admin.action(description=_("Mark selected users as active"))
    def make_active(self, request, queryset):
        """Mark selected users as active."""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            _(f"{updated} users were successfully marked as active."),
        )

    @admin.action(description=_("Mark selected users as inactive"))
    def make_inactive(self, request, queryset):
        """Mark selected users as inactive."""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            _(f"{updated} users were successfully marked as inactive."),
        )

    @admin.action(description=_("Verify email addresses for selected users"))
    def verify_emails(self, request, queryset):
        """Verify email addresses for selected users."""
        updated = 0
        for user in queryset:
            if not user.is_verified:
                user.verify_email()
                updated += 1
        self.message_user(
            request,
            _(f"{updated} user email addresses were successfully verified."),
        )

    @admin.action(description=_("Send welcome email to selected users"))
    def send_welcome_email(self, request, queryset):
        """Send welcome email to selected users."""
        sent = 0
        for user in queryset:
            try:
                user.email_user(
                    subject=_("Welcome to our platform!"),
                    message=_(
                        f"Hello {user.get_full_name()},\n\n"
                        "Welcome to our platform! "
                        "We're excited to have you on board.\n\n"
                        "Best regards,\nThe Team"
                    ),
                )
                sent += 1
            except Exception:
                pass  # Continue with other users if one fails
        self.message_user(
            request,
            _(f"Welcome email sent to {sent} users."),
        )
