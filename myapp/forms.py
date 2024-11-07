# forms.py
from django import forms
from .models import PersonInfo, Cloth


class PersonInfoForm(forms.ModelForm):
    class Meta:
        model = PersonInfo
        fields = ['sex', 'height', 'weight', 'province', 'city']

class ClothForm(forms.ModelForm):
    class Meta:
        model = Cloth
        fields = ['title','category', 'color', 'image']