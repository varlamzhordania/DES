from django.urls import path
from .views import login_view

app_name = 'account'

urlpatterns = [
    path("auth/login/", login_view, name="login"),
    # path("auth/logout/"),
]
