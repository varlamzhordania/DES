from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category, Food
from checkout.models import Order


# Create your views here.

@login_required
def home(request, *args, **kwargs):
    sessions = request.user.session_set.all().first()
    print(sessions.get_decoded())
    print(Order.objects.filter(session_id=request.session.get('session_id')))
    my_context = {
        "Title": "Home",
    }
    return render(request, "main/home.html", my_context)

@login_required
def support(request, *args, **kwargs):
    my_context = {
        "Title": "Support"
    }
    return render(request, "stream/call.html", my_context)
