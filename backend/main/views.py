from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def home(request, *args, **kwargs):
    my_context = {
        "Title": "DES Project"
    }
    return render(request, "main.html", my_context)
