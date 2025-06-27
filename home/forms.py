from django import forms
from .models import FeedbackModel

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedbackModel
        fields = '__all__'
        widgets = {
            'rater':forms.HiddenInput(),
            'rating': forms.HiddenInput(),
            'comments': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }