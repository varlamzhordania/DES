from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from account.models import Seat


class CustomerForm(forms.ModelForm):
    first_name = forms.CharField(
        label=_("Full Name"),
        max_length=50,
        help_text=_("example : john doe"),
        widget=forms.TextInput(attrs={'class': "form-control", "id": "full_name"})
    )

    class Meta:
        model = get_user_model()
        fields = ['first_name']


class SeatForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput())
    seat_number = forms.IntegerField(
        required=False,
        disabled=True,
        label=_("Seat Number"),
        min_value=0,
        widget=forms.TextInput(attrs={'class': 'form-control', "readonly": True})
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
        fields = ["id", "seat_number", "seat_name"]
        read_only_fields = ["id", "seat_number"]


SeatFormSet = forms.modelformset_factory(Seat, form=SeatForm, extra=0)
