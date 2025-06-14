from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form with additional fields."""

    email = forms.EmailField(
        required=True,
        help_text=_("Required. Enter a valid email address."),
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    first_name = forms.CharField(
        max_length=150,
        required=False,
        help_text=_("Optional. 150 characters or fewer."),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    last_name = forms.CharField(
        max_length=150,
        required=False,
        help_text=_("Optional. 150 characters or fewer."),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    phone_number = forms.CharField(
        max_length=17,
        required=False,
        help_text=_("Optional. Phone number in international format."),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    date_of_birth = forms.DateField(
        required=False,
        help_text=_("Optional. Your date of birth."),
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "date_of_birth",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to password fields
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})

    def clean_email(self):
        """Validate that the email is unique."""
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise ValidationError(
                _("A user with this email address already exists.")
            )
        return email

    def save(self, commit=True):
        """Save the user with the provided information."""
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.date_of_birth = self.cleaned_data["date_of_birth"]
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Custom authentication form with styling."""

    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter your email"),
                "autofocus": True,
            }
        ),
    )

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter your password"),
                "autocomplete": "current-password",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update the username field to use email
        self.fields["username"].label = _("Email")


class CustomPasswordResetForm(PasswordResetForm):
    """Custom password reset form with styling."""

    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter your email address"),
                "autocomplete": "email",
            }
        ),
    )

    def get_users(self, email):
        """Return matching user(s) who should receive a reset."""
        active_users = User.objects.filter(email__iexact=email, is_active=True)
        return (
            user
            for user in active_users
            if user.has_usable_password()
            and user.email == email  # Exact match for security
        )


class CustomSetPasswordForm(SetPasswordForm):
    """Custom set password form with styling."""

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter new password"),
                "autocomplete": "new-password",
            }
        ),
        strip=False,
    )

    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Confirm new password"),
                "autocomplete": "new-password",
            }
        ),
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom password change form with styling."""

    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter current password"),
                "autocomplete": "current-password",
                "autofocus": True,
            }
        ),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter new password"),
                "autocomplete": "new-password",
            }
        ),
        strip=False,
    )

    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Confirm new password"),
                "autocomplete": "new-password",
            }
        ),
    )


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information."""

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "date_of_birth",
            "preferred_language",
            "timezone_preference",
            "email_notifications",
            "marketing_emails",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "preferred_language": forms.Select(attrs={"class": "form-select"}),
            "timezone_preference": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "email_notifications": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "marketing_emails": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add help text to fields
        self.fields["phone_number"].help_text = _(
            "Phone number in international format (e.g., +1234567890)"
        )

        self.fields["email_notifications"].help_text = _(
            "Receive notifications about important account updates"
        )
        self.fields["marketing_emails"].help_text = _(
            "Receive promotional emails and newsletters"
        )

    def clean_phone_number(self):
        """Validate phone number format."""
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number:
            # Basic validation for international format
            import re

            pattern = r"^\+?1?\d{9,15}$"
            if not re.match(pattern, phone_number):
                raise ValidationError(
                    _(
                        "Enter a valid phone number in international format "
                        "(e.g., +1234567890)"
                    )
                )
        return phone_number


class EmailVerificationForm(forms.Form):
    """Form for email verification."""

    email = forms.EmailField(
        label=_("Email Address"),
        help_text=_("Enter your email address to resend verification."),
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter your email address"),
            }
        ),
    )

    def clean_email(self):
        """Validate that the email exists and is not already verified."""
        email = self.cleaned_data.get("email")
        try:
            user = User.objects.get(email=email)
            if user.is_verified:
                raise ValidationError(_("This email is already verified."))
        except User.DoesNotExist:
            raise ValidationError(
                _("No account found with this email address.")
            )
        return email


class ContactForm(forms.Form):
    """Generic contact form."""

    name = forms.CharField(
        max_length=100,
        label=_("Full Name"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter your full name"),
            }
        ),
    )

    email = forms.EmailField(
        label=_("Email Address"),
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter your email address"),
            }
        ),
    )

    subject = forms.CharField(
        max_length=200,
        label=_("Subject"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter message subject"),
            }
        ),
    )

    message = forms.CharField(
        label=_("Message"),
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": _("Enter your message"),
            }
        ),
    )

    def send_email(self):
        """Send the contact form email."""
        # This would typically integrate with your email service
        # For now, it's a placeholder for the email sending logic
        # Implementation would use self.cleaned_data
        pass
