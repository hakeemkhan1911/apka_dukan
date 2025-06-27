from django import forms
from .models import RegisterKarigarModel

class RegisterKarigarForm(forms.ModelForm):
    class Meta:
        model = RegisterKarigarModel
        fields='__all__'
        widgets={
            'karigar_shop':forms.HiddenInput,
            'fake_id':forms.HiddenInput,
            'password':forms.PasswordInput,
            'password_again':forms.PasswordInput,
            'status':forms.HiddenInput,
        }