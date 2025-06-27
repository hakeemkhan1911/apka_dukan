from django import forms
from .models import SellProductModel,ImageModel,MessagesModel

class SellProductForm(forms.ModelForm):
    class Meta:
        model = SellProductModel
        fields='__all__'
        widgets={
            'owner':forms.HiddenInput,
        }
class ImageForm(forms.ModelForm):
    class Meta:
        model=ImageModel
        fields='__all__'
        widgets={
            'product_info':forms.HiddenInput,
        }
class MessagesForm(forms.ModelForm):
    class Meta:
        model=MessagesModel
        fields=['message']
        