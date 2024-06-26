from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .decorators import unauthenticated_user
from core.utils import fancy_message
from .utils import set_new_session
import logging


# Create your views here.


@unauthenticated_user
def login_view(request, *args, **kwargs):
    next_url = request.GET.get('next', None)
    if request.method == 'POST':
        try:
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            next_url = request.POST.get('next_url', None)
            if username and password:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    if next_url and next_url != "None":
                        set_new_session(request)
                        fancy_message(request, f"Welcome back {user.username}", "success")
                        return redirect(next_url)
                    else:
                        return redirect("main:home")
                else:
                    fancy_message(request, "Invalid username or password.", "error")
            else:
                fancy_message(request, "Username and password is required", "error")
        except Exception as e:
            fancy_message(request, "Login process failed, please try later", "error")

    my_context = {
        "Title": "Login",
        "next_url": next_url
    }
    return render(request, "account/login.html", my_context)


@login_required
def logout_view(request, *args, **kwargs):
    logout(request)
    fancy_message(request, f"You have been logged out.", "success")
    return redirect("main:home")
