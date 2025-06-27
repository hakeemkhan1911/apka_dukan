from django import forms
from .models import AddShopModel

class AddShopForm(forms.ModelForm):
    class Meta:
        model = AddShopModel
        fields='__all__'
        widgets={
            'shop_owner':forms.HiddenInput,
            'booking':forms.HiddenInput,
            'karigar_requests':forms.HiddenInput,
            
        }
