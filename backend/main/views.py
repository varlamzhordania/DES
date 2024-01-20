from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category, Food


# Create your views here.

@login_required
def home(request, *args, **kwargs):
    categories = Category.objects.filter(is_active=True)
    category = request.GET.get("category", None)
    foods = Food.objects.all()
    if category:
        foods = foods.filter(category__slug=category)
    my_context = {
        "Title": "DES Project",
        "categories": categories,
        "foods": foods
    }
    return render(request, "main/home.html", my_context)
