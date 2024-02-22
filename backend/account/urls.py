from django.urls import path
from .views import login_view,logout_view
from .api import UserDetail

app_name = 'account'

urlpatterns = [
    path("auth/login/", login_view, name="login"),
    path("auth/logout/", logout_view, name="logout"),
    path("api/user/", UserDetail.as_view(), name="user_detail")
]
