from django import forms
from .models import AddOrderModel

class AddOrderForm(forms.ModelForm):
    class Meta:
        model = AddOrderModel
        fields='__all__'
        widgets={
            'customer':forms.HiddenInput,
        }