from django import forms
from .models import Data


class UploadForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ('image',)
