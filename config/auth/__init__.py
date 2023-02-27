from django.contrib.auth import backends, get_user_model
from django.db.models import Q


class EmailUsername(backends.ModelBackend):
    def authenticate(self, request, username: str = "", password: str = "", **kwargs):
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )

            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
