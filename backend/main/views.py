from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Food
from checkout.models import Order
from .forms import CustomerForm, SeatFormSet
from account.models import Seat
from core.utils import fancy_message


# Create your views here.

@login_required
def home_view(request, *args, **kwargs):
    sessions = request.user.session_set.all().first()

    print(sessions.get_decoded())
    print(Order.objects.filter(session_id=request.session.get('session_id')))

    my_context = {
        "Title": "Home",
    }
    return render(request, "main/home.html", my_context)


@login_required
def support_view(request, *args, **kwargs):
    my_context = {
        "Title": "Support"
    }
    return render(request, "stream/call.html", my_context)


@login_required
def settings_view(request, *args, **kwargs):
    customer_form = CustomerForm(instance=request.user)
    seat_form_set = SeatFormSet(queryset=Seat.objects.filter(user=request.user))

    if request.method == "POST":
        customer_form = CustomerForm(instance=request.user, data=request.POST)
        seat_form_set = SeatFormSet(queryset=Seat.objects.filter(user=request.user), data=request.POST)

        if customer_form.is_valid() and seat_form_set.is_valid():
            customer_obj = customer_form.save()
            seat_form_set.save()
            request.session['customer'] = customer_obj.get_name()
            fancy_message(request, "New settings have been saved.", "success")
            return redirect('main:settings')
        else:
            fancy_message(request, "There was an error saving your settings. Please check the form.", "error")

    my_context = {
        "Title": "Settings",
        "customer_form": customer_form,
        "formset": seat_form_set
    }
    return render(request, "main/settings.html", my_context)
