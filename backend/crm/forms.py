from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from account.models import Seat
from main.models import Food, Category
from settings.models import Theme, Setting


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        exclude = "__all__"
        widgets = {
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "logo_mini": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "payment_gateways": forms.CheckboxSelectMultiple(attrs={"class": "form-check-box"}),
            "payment_gateway_details": forms.SelectMultiple(attrs={"class": "form-control"}),
        }


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        exclude = ['is_primary']
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "primary_color": forms.TextInput(attrs={"class": "form-control"}),
            "secondary_color": forms.TextInput(attrs={"class": "form-control"}),
            "success_color": forms.TextInput(attrs={"class": "form-control"}),
            "info_color": forms.TextInput(attrs={"class": "form-control"}),
            "warning_color": forms.TextInput(attrs={"class": "form-control"}),
            "danger_color": forms.TextInput(attrs={"class": "form-control"}),
            "light_color": forms.TextInput(attrs={"class": "form-control"}),
            "dark_color": forms.TextInput(attrs={"class": "form-control"}),
            "body_bg_color": forms.TextInput(attrs={"class": "form-control"}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'


class UserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=50,
        disabled=True,
        required=True,
        label=_("Username"),
        widget=forms.TextInput(attrs={'class': "form-control", 'readonly': "true", })
    )
    first_name = forms.CharField(
        max_length=50,
        label=_("Alias Name"),
        widget=forms.TextInput(attrs={'class': "form-control", "placeholder": _("Alias Name")})
    )
    is_staff = forms.BooleanField(
        label=_("Staff"),
        widget=forms.CheckboxInput(attrs={'class': "form-check-input", })
    )
    is_active = forms.BooleanField(
        label=_("Active"),
        widget=forms.CheckboxInput(attrs={'class': "form-check-input", })
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', "is_staff", "is_active"]


class SeatForm(forms.ModelForm):
    # id = forms.IntegerField(widget=forms.HiddenInput())
    seat_number = forms.IntegerField(
        required=False,
        label=_("Seat Number"),
        min_value=0,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    seat_name = forms.CharField(
        max_length=50,
        required=False,
        label=_("Seat Name"),
        help_text=_("name of the person who seat on that chair"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Seat
        fields = ["seat_number", "seat_name"]


SeatFormSet = forms.modelformset_factory(Seat, form=SeatForm, extra=3)
