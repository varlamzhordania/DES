from django.shortcuts import render


# Create your views here.


def dashboard_view(request, *args, **kwargs):
    my_context = {
        "Title": "Dashboard"
    }

    return render(request, "crm/dashboard.html", my_context)
