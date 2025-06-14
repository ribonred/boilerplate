from django.urls import include, path

app_name = 'v1'

urlpatterns = [
    path("auth/", include("apis.v1.user.urls")),
]
