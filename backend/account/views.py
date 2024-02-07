from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .decorators import unauthenticated_user
from core.utils import fancy_message
import logging
import uuid


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
                        request.session["session_id"] = str(uuid.uuid4())
                        request.session["customer"] = username
                        fancy_message(request, f"Welcome back {user.username}", "success")
                        return redirect(next_url)
                    else:
                        return redirect("main:home")
                else:
                    fancy_message(request, "Invalid username or password.", "error")
            else:
                fancy_message(request, "Username and password is required", "error")
        except Exception as e:
            logging.error(e)
    my_context = {
        "Title": "Login",
        "next_url": next_url
    }
    return render(request, "account/login.html", my_context)