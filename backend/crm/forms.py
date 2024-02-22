from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from account.models import Seat
from main.models import Food, Category
from settings.models import Theme, Setting
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from checkout.models import Tip, Extra, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"


class ExtraForm(forms.ModelForm):
    class Meta:
        model = Extra
        fields = '__all__'
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = '__all__'
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


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
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "example : Sea food"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ["name", "description", "category", "thumbnail", "price", "ingredients", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "example : burger"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "thumbnail": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "ingredients": forms.Textarea(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class UserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=50,
        disabled=True,
        required=True,
        label=_("Username"),
        widget=forms.TextInput(attrs={'class': "form-control", 'readonly': "true", })
    )
    first_name = forms.CharField(
        required=False,
        max_length=50,
        label=_("Alias Name"),
        widget=forms.TextInput(attrs={'class': "form-control", "placeholder": _("Alias Name")})
    )
    is_staff = forms.BooleanField(
        label=_("Staff"),
        required=False,
        widget=forms.CheckboxInput(attrs={'class': "form-check-input", })
    )
    is_active = forms.BooleanField(
        label=_("Active"),
        required=False,
        widget=forms.CheckboxInput(attrs={'class': "form-check-input", })
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', "groups", "is_staff", "is_active"]
        widgets = {
            "groups": forms.SelectMultiple(attrs={"class": "form-select"}),
        }


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    is_staff = forms.BooleanField(
        label=_("Staff"),
        required=False,
        widget=forms.CheckboxInput(attrs={'class': "form-check-input", })
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "password1", "password2", "groups", "is_staff"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "groups": forms.SelectMultiple(attrs={"class": "form-select"}),
        }


class SeatForm(forms.ModelForm):
    class Meta:
        model = Seat
        fields = ["seat_number", "seat_name"]
        widgets = {
            "seat_number": forms.NumberInput(attrs={'class': "form-control", "placeholder": "example 1,2...etc"}),
            "seat_name": forms.NumberInput(attrs={'class': "form-control", "placeholder": "example john doe"}),
        }


SeatFormSet = forms.inlineformset_factory(
    get_user_model(),
    Seat,
    form=SeatForm,
    extra=0,
    can_delete=True,
    can_delete_extra=False
)
