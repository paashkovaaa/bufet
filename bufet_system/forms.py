from django import forms
from bufet_system.models import Order, Restaurant


class OrderForm(forms.ModelForm):
    restaurant = forms.ModelChoiceField(
        queryset=Restaurant.objects.all(),
        widget=forms.RadioSelect,
    )

    class Meta:
        model = Order
        fields = ["restaurant"]


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
