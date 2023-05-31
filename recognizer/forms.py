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
        # widgets = {'name' : forms.TextInput(attrs={'class':'form-input', 'style' : 'margin 50px'}),
        #            'feedback' : forms.Textarea(attrs={'style': 'background-color: yellow;', 'cols': 100, 'rows' : 10})}




