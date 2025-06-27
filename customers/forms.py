from django import forms
from .models import AddCustomerModel

class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = AddCustomerModel
        fields='__all__'
        widgets={
            'shop':forms.HiddenInput,
            'password':forms.PasswordInput,
        }