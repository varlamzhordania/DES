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
        "Title": "DES Project",
    }
    return render(request, "main/home.html", my_context)
