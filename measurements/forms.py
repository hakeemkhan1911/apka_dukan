from django import forms
from .models import AddMeasurementModel

class AddMeasurementForm(forms.ModelForm):
    class Meta:
        model = AddMeasurementModel
        fields='__all__'
        widgets={
            'customer':forms.HiddenInput,
        }