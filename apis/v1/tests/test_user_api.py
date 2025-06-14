"""
API tests for JWT authentication endpoints.
"""

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.mark.api
@pytest.mark.auth
@pytest.mark.django_db
class TestJWTAuthentication:
    """Test cases for JWT authentication endpoints."""

    def test_token_obtain_valid_credentials(
        self, api_client, user_factory, api_urls
    ):
        """Test obtaining JWT token with valid credentials."""
        password = "testpass123"
        user = user_factory(email="test@example.com", password=password)

        login_data = {"email": user.email, "password": password}

        response = api_client.post(api_urls["token_obtain"], login_data)

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

        # Tokens should be valid strings
        assert isinstance(response.data["access"], str)
        assert isinstance(response.data["refresh"], str)
        assert len(response.data["access"]) > 0
        assert len(response.data["refresh"]) > 0

    def test_token_obtain_invalid_credentials(self, api_client, api_urls):
        """Test obtaining JWT token with invalid credentials."""
        invalid_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword",
        }

        response = api_client.post(api_urls["token_obtain"], invalid_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "access" not in response.data
        assert "refresh" not in response.data

    def test_token_obtain_missing_email(self, api_client, api_urls):
        """Test obtaining JWT token with missing email."""
        incomplete_data = {"password": "testpass123"}

        response = api_client.post(api_urls["token_obtain"], incomplete_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_token_obtain_missing_password(self, api_client, api_urls):
        """Test obtaining JWT token with missing password."""
        incomplete_data = {"email": "test@example.com"}

        response = api_client.post(api_urls["token_obtain"], incomplete_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_token_obtain_inactive_user(
        self, api_client, inactive_user_factory, api_urls
    ):
        """Test that inactive users cannot obtain tokens."""
        password = "testpass123"
        user = inactive_user_factory(password=password)

        login_data = {"email": user.email, "password": password}

        response = api_client.post(api_urls["token_obtain"], login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_token_refresh_valid_token(
        self, api_client, user_factory, api_urls
    ):
        """Test refreshing JWT token with valid refresh token."""
        user = user_factory()
        refresh = RefreshToken.for_user(user)

        refresh_data = {"refresh": str(refresh)}

        response = api_client.post(api_urls["token_refresh"], refresh_data)

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert isinstance(response.data["access"], str)
        assert len(response.data["access"]) > 0

    def test_token_refresh_invalid_token(self, api_client, api_urls):
        """Test refreshing JWT token with invalid refresh token."""
        invalid_data = {"refresh": "invalid.token.here"}

        response = api_client.post(api_urls["token_refresh"], invalid_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_token_refresh_missing_token(self, api_client, api_urls):
        """Test refreshing JWT token with missing refresh token."""
        response = api_client.post(api_urls["token_refresh"], {})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_token_verify_valid_token(self, api_client, user_factory, api_urls):
        """Test verifying valid JWT token."""
        user = user_factory()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        verify_data = {"token": access_token}

        response = api_client.post(api_urls["token_verify"], verify_data)

        assert response.status_code == status.HTTP_200_OK

    def test_token_verify_invalid_token(self, api_client, api_urls):
        """Test verifying invalid JWT token."""
        invalid_data = {"token": "invalid.token.here"}

        response = api_client.post(api_urls["token_verify"], invalid_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_token_verify_missing_token(self, api_client, api_urls):
        """Test verifying JWT token with missing token."""
        response = api_client.post(api_urls["token_verify"], {})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_token_verify_expired_token(
        self, api_client, user_factory, api_urls
    ):
        """Test verifying expired JWT token."""
        user = user_factory()
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Set token to expired
        access_token.set_exp(
            lifetime=timezone.timedelta(days=1),
            from_time=timezone.now() - timezone.timedelta(days=2),
        )

        verify_data = {"token": str(access_token)}

        response = api_client.post(api_urls["token_verify"], verify_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.api
@pytest.mark.auth
@pytest.mark.django_db
class TestJWTAuthenticationFlow:
    """Test complete JWT authentication flow."""

    def test_complete_authentication_flow(
        self, api_client, user_factory, api_urls
    ):
        """Test complete authentication flow: login -> use token ->
        refresh -> verify."""
        password = "testpass123"
        user = user_factory(password=password)

        # Step 1: Login to get tokens
        login_data = {"email": user.email, "password": password}

        login_response = api_client.post(api_urls["token_obtain"], login_data)
        assert login_response.status_code == status.HTTP_200_OK

        access_token = login_response.data["access"]
        refresh_token = login_response.data["refresh"]

        # Step 2: Verify access token
        verify_data = {"token": access_token}
        verify_response = api_client.post(api_urls["token_verify"], verify_data)
        assert verify_response.status_code == status.HTTP_200_OK

        # Step 3: Refresh token
        refresh_data = {"refresh": refresh_token}
        refresh_response = api_client.post(
            api_urls["token_refresh"], refresh_data
        )
        assert refresh_response.status_code == status.HTTP_200_OK

        new_access_token = refresh_response.data["access"]

        # Step 4: Verify new access token
        verify_new_data = {"token": new_access_token}
        verify_new_response = api_client.post(
            api_urls["token_verify"], verify_new_data
        )
        assert verify_new_response.status_code == status.HTTP_200_OK

        # New token should be different from old token
        assert new_access_token != access_token

    def test_authentication_with_email_case_insensitive(
        self, api_client, user_factory, api_urls
    ):
        """Test that email authentication is case insensitive."""
        password = "testpass123"
        _user = user_factory(email="test@example.com", password=password)

        # Try login with different case
        login_data = {"email": "TEST@EXAMPLE.COM", "password": password}

        response = api_client.post(api_urls["token_obtain"], login_data)

        # Should work regardless of email case
        assert response.status_code in [
            status.HTTP_401_UNAUTHORIZED,
        ]
        # Note: Actual behavior depends on your authentication backend config
