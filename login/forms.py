from django import forms
from .models import LoginModel

class LoginForm(forms.ModelForm):
    class Meta:
        model = LoginModel
        fields='__all__'
        widgets={
            'password':forms.PasswordInput,
            'password_again':forms.PasswordInput,
            'full_name':forms.HiddenInput,
            'fake_id':forms.HiddenInput,
            'status':forms.HiddenInput,
            'karigar_requests':forms.HiddenInput,
            
        }