from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from core.utils import is_admin


# Create your views here.

@login_required
@user_passes_test(is_admin)
def dashboard_view(request, *args, **kwargs):
    my_context = {
        "Title": "Dashboard"
    }

    return render(request, "crm/dashboard.html", my_context)
