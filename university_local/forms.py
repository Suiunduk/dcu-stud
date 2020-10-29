from django import forms
from .models import University


class UniversityData(forms.Form):
    class meta:
        model = University
        fields = '__all__'
