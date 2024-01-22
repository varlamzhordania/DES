from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category, Food


# Create your views here.

@login_required
def home(request, *args, **kwargs):
    categories = Category.objects.filter(is_active=True)
    category_param = request.GET.get("category", None)
    foods = Food.objects.all()
    if category_param:
        foods = foods.filter(category__slug=category_param)
    my_context = {
        "Title": "DES Project",
        "categories": categories,
        "foods": foods,
        "category_param": category_param,
    }
    return render(request, "main/home.html", my_context)
