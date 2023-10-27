from django import forms
from .models import *

class ClassByRecognizerForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['image']

class ClassByUserForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['class_by_user']
        widgets = {
            'class_by_user': forms.Select(attrs={'class': 'my-select-style'})
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'feedback']





