from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from account.utils import is_manager_user
from stream.models import UserRoom
from main.models import Food, Category
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.utils import fancy_message
from .forms import UserForm, SeatFormSet, FoodForm, CategoryForm, ThemeForm, SettingForm, CustomUserCreationForm, \
    TipForm, ExtraForm, OrderForm
from settings.models import Theme, Setting
from django.db import transaction
from django.views.decorators.http import require_POST
from checkout.models import Extra, Tip, Order


# Create your views here.

@login_required
@user_passes_test(is_manager_user)
def dashboard_view(request, *args, **kwargs):
    my_context = {
        "Title": "Dashboard"
    }

    return render(request, "crm/dashboard.html", my_context)


@login_required
@user_passes_test(is_manager_user)
def users_list_view(request, *args, **kwargs):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            fancy_message(request, "User successfully created!", "success")
            return redirect(".")
        else:
            fancy_message(request, form.errors, "error")

    queryset = get_user_model().objects.all()

    page = request.GET.get('page')

    items_per_page = 10
    paginator = Paginator(queryset, items_per_page)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    form = CustomUserCreationForm()
    my_context = {
        "Title": "Account List",
        "users": users,
        "page": page,
        "form": form,
    }

    return render(request, "crm/users/users_list.html", my_context)


@login_required
@user_passes_test(is_manager_user)
def users_detail_view(request, pk, *args, **kwargs):
    user = get_object_or_404(get_user_model(), id=pk)
    form = UserForm(instance=user)
    formset = SeatFormSet(instance=user)
    if request.method == "POST":
        form = UserForm(instance=user, data=request.POST)
        formset = SeatFormSet(instance=user, data=request.POST)
        print(request.POST)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            fancy_message(request, "Changes saved successfully", level="success")
            return redirect(".")
        else:
            fancy_message(request, form.errors, level="error")
            fancy_message(request, formset.errors, level="error")

    my_context = {
        "Title": user.username,
        "form": form,
        "formset": formset
    }
    return render(request, "crm/users/users_detail.html", my_context)


@login_required
@user_passes_test(is_manager_user)
def orders_list_view(request, *args, **kwargs):
    if request.method == "POST":
        form = OrderForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            fancy_message(request, "Order successfully created!", "success")
            return redirect(".")
        else:
            fancy_message(request, form.errors, "error")
    queryset = Order.objects.all()

    items_per_page = 10

    paginator = Paginator(queryset, items_per_page)

    page = request.GET.get('page')

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    form = OrderForm()

    my_context = {
        "Title": "Order List",
        "orders": orders,
        "page": page,
        "form": form
    }

    return render(request, "crm/orders/orders_list.html", my_context)


@login_required
@user_passes_test(is_manager_user)
def orders_detail_view(request, pk, *args, **kwargs):
    order = get_object_or_404(Order, id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(instance=order, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            fancy_message(request, "Changes saved successfully", level="success")
            return redirect(".")
        else:
            fancy_message(request, form.errors, level="error")

    my_context = {
        "Title": order.id,
        "order": order,
        "form": form,
    }
    return render(request, "crm/orders/orders_detail.html", my_context)


@login_required
@user_passes_test(is_manager_user)
def foods_list_view(request, *args, **kwargs):
    if request.method == "POST":
        form = FoodForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            fancy_message(request, "Food successfully created!", "success")
            return redirect(".")
        else:
            fancy_message(request, form.errors, "error")
    queryset = Food.objects.all()

    items_per_page = 10

    paginator = Paginator(queryset, items_per_page)

    page = request.GET.get('page')

    try:
        foods = paginator.page(page)
    except PageNotAnInteger:
        foods = paginator.page(1)
    except EmptyPage:
        foods = paginator.page(paginator.num_pages)

    form = FoodForm()

    my_context = {
        "Title": "Food List",
        "foods": foods,
        "page": page,
        "form": form
    }

    return render(request, "crm/foods/foods_list.html", my_context)


@login_required
@user_passes_test(is_manager_user)
def foods_detail_view(request, pk, *args, **kwargs):
    food = get_object_or_404(Food, id=pk)
    form = FoodForm(instance=food)
    if request.method == "POST":
        form = FoodForm(instance=food, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            fancy_message(request, "Changes saved successfully", level="success")
            return redirect(".")
        else:
            fancy_message(request, form.errors, level="error")

    my_context = {
        "Title": food.name,
        "form": form,
    }
    return render(request, "crm/foods/foods_detail.html", my_context)


@require_POST
@login_required
@user_passes_test(is_manager_user)
def food_delete_view(request, *args, **kwargs):
    id = request.POST.get("food-id")
    food = get_object_or_404(Food, id=id)
    food.delete()
    fancy_message(request, "Food Deleted", level="success")
    return redirect("crm:foods_list")


@login_required
@user_passes_test(is_manager_user)
def categories_list_view(request, *args, **kwargs):
    if request.method == "POST":
        form = CategoryForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            fancy_message(request, "Food successfully created!", "success")
            return redirect(".")
        else:
            fancy_message(request, form.errors, "error")

    queryset = Category.objects.all()

    items_per_page = 10

    paginator = Paginator(queryset, items_per_page)

    page = request.GET.get('page')

    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    form = CategoryForm()

    my_context = {
        "Title": "category List",
        "categories": categories,
        "page": page,
        "form": form,
    }

    return render(request, "crm/categories/categories_list.html", my_context)


@login_required
@user_passes_test(is_manager_user)
def categories_detail_view(request, pk, *args, **kwargs):
    category = get_object_or_404(Category, id=pk)
    form = CategoryForm(instance=category)
    if request.method == "POST":
        form = CategoryForm(instance=category, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            fancy_message(request, "Changes saved successfully", level="success")
            return redirect(".")
        else:
            fancy_message(request, form.errors, level="error")

    my_context = {
        "Title": category.name,
        "form": form,
    }
    return render(request, "crm/categories/categories_detail.html", my_context)


@require_POST
@login_required
@user_passes_test(is_manager_user)
def category_delete_view(request, *args, **kwargs):
    id = request.POST.get("category-id")
    category = get_object_or_404(Category, id=id)
    category.delete()
    fancy_message(request, "Category Deleted", level="success")
    return redirect("crm:categories_list")


@login_required
@user_passes_test(is_manager_user)
def tips_list_view(request, *args, **kwargs):
    if request.method == "POST":
        form = TipForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            fancy_message(request, "Tip successfully created!", "success")
            return redirect(".")
        else:
            fancy_message(request, form.errors, "error")

    queryset = Tip.objects.all().order_by("-id")

    items_per_page = 10

    paginator = Paginator(queryset, items_per_page)

    page = request.GET.get('page')

    try:
        tips = paginator.page(page)
    except PageNotAnInteger:
        tips = paginator.page(1)
    except EmptyPage:
        tips = paginator.page(paginator.num_pages)

    form = TipForm()

    my_context = {
        "Title": "Tip List",
        "tips": tips,
        "page": page,
        "form": form,
    }

    return render(request, "crm/tips/tips_list.html", my_context)


@login_required
@user_passes_test(is_manager_user)
def tips_detail_view(request, pk, *args, **kwargs):
    tip = get_object_or_404(Tip, id=pk)
    form = TipForm(instance=tip)
    if request.method == "POST":
        form = TipForm(instance=tip, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            fancy_message(request, "Changes saved successfully", level="success")
            return redirect(".")
        else:
            fancy_message(request, form.errors, level="error")

    my_context = {
        "Title": tip.name,
        "form": form,
    }
    return render(request, "crm/tips/tips_detail.html", my_context)


@require_POST
@login_required
@user_passes_test(is_manager_user)
def tips_delete_view(request, *args, **kwargs):
    id = request.POST.get("tip-id")
    tip = get_object_or_404(Tip, id=id)
    tip.delete()
    fancy_message(request, "Tip Deleted", level="success")
    return redirect("crm:tips_list")


@login_required
@user_passes_test(is_manager_user)
def extras_list_view(request, *args, **kwargs):
    if request.method == "POST":
        form = ExtraForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            fancy_message(request, "Extra successfully created!", "success")
            return redirect(".")
        else:
            fancy_message(request, form.errors, "error")

    queryset = Extra.objects.all().order_by("-id")

    items_per_page = 10

    paginator = Paginator(queryset, items_per_page)

    page = request.GET.get('page')

    try:
        extras = paginator.page(page)
    except PageNotAnInteger:
        extras = paginator.page(1)
    except EmptyPage:
        extras = paginator.page(paginator.num_pages)

    form = ExtraForm()

    my_context = {
        "Title": "Extra List",
        "extras": extras,
        "page": page,
        "form": form,
    }

    return render(request, "crm/extras/extras_list.html", my_context)


@login_required
@user_passes_test(is_manager_user)
def extras_detail_view(request, pk, *args, **kwargs):
    extra = get_object_or_404(Extra, id=pk)
    form = ExtraForm(instance=extra)
    if request.method == "POST":
        form = ExtraForm(instance=extra, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            fancy_message(request, "Changes saved successfully", level="success")
            return redirect(".")
        else:
            fancy_message(request, form.errors, level="error")

    my_context = {
        "Title": extra.name,
        "form": form,
    }
    return render(request, "crm/extras/extras_detail.html", my_context)


@require_POST
@login_required
@user_passes_test(is_manager_user)
def extras_delete_view(request, *args, **kwargs):
    id = request.POST.get("extra-id")
    extra = get_object_or_404(Extra, id=id)
    extra.delete()
    fancy_message(request, "Extra Deleted", level="success")
    return redirect("crm:extras_list")


@login_required
@user_passes_test(is_manager_user)
def settings_view(request, *args, **kwargs):
    themes = Theme.objects.all()
    primary_theme = themes.filter(is_primary=True).first()
    theme_form = ThemeForm(instance=primary_theme)

    setting = Setting.objects.first()
    setting_form = SettingForm(instance=setting)

    if request.method == "POST":
        setting_form = SettingForm(instance=setting, data=request.POST)
        if setting_form.is_valid():
            setting_form.save()
            fancy_message(request, "Changes saved successfully", level="success")
            return redirect(".")
        else:
            fancy_message(request, setting_form.errors, level="error")
    my_context = {
        "Title": "Settings",
        "themes": themes,
        "primary_theme": primary_theme,
        "theme_form": theme_form,
        "setting_form": setting_form
    }

    return render(request, "crm/settings/settings.html", my_context)


@require_POST
@login_required
@user_passes_test(is_manager_user)
def settings_theme_view(request):
    themes = Theme.objects.all()
    theme_id = int(request.POST.get("theme", None))
    if theme_id != 0:
        data = {
            "id": theme_id,
            "name": request.POST.get("name"),
            "primary_color": request.POST.get("primary_color"),
            "secondary_color": request.POST.get("secondary_color"),
            "success_color": request.POST.get("success_color"),
            "info_color": request.POST.get("info_color"),
            "warning_color": request.POST.get("warning_color"),
            "danger_color": request.POST.get("danger_color"),
            "light_color": request.POST.get("light_color"),
            "dark_color": request.POST.get("dark_color"),
            "body_bg_color": request.POST.get("body_bg_color"),
        }
        theme_instance = themes.get(id=theme_id)
        form = ThemeForm(instance=theme_instance, data=data)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.is_primary = True
            obj.save()
            fancy_message(request, "Theme changes successfully saved", "success")
        else:
            fancy_message(request, form.errors, "error")
    else:
        if themes.filter(is_primary=True).exists():
            theme_instance = themes.filter(is_primary=True).first()
            theme_instance.is_primary = False
            theme_instance.save()
        fancy_message(request, "Theme changes successfully saved", "success")
    return redirect("crm:dashboard_settings")


@login_required
@user_passes_test(is_manager_user)
def support_view(request, pk, *args, **kwargs):
    try:
        queryset = UserRoom.objects.get(pk=pk)
        my_context = {
            "Title": "Support",
            "room": queryset,
        }
        return render(request, "stream/call.html", my_context)
    except UserRoom.DoesNotExist:
        my_context = {
            "Title": "Support",
            "room": None
        }
        return render(request, "stream/call.html", my_context)
