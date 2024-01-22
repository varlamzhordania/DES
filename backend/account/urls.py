from django.urls import path
from .views import login_view
from .api import UserDetail

app_name = 'account'

urlpatterns = [
    path("auth/login/", login_view, name="login"),
    path("api/user/", UserDetail.as_view(), name="user_detail")
]
