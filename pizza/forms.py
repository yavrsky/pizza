from django.forms import ModelForm, Form
from django import forms
from .models import *
import re

class ComponentForm(forms.Form):
    number = forms.IntegerField(min_value=0, label='')

class IngredientForm(forms.Form):
    obj = Ingredient.objects.get(type='rad')

    CHOICES = [(i.name, i.name) for i in obj.component_set.all()]
    type = forms.ChoiceField(
        label=obj.title,
        widget=forms.RadioSelect(),
        choices=CHOICES,
        initial=CHOICES[0][0]
        )


class ContactForm(forms.Form):
    person_name = forms.CharField()
    email = forms.EmailField()
    phone_number = forms.CharField()

    def clean_person_name(self):
        data = self.cleaned_data['person_name']
        if not re.fullmatch(r'[A-Z][a-z]+', data):
            raise forms.ValidationError("Your name must starts with capitalize letter")
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if not re.fullmatch(r'\w+@gmail.com', data):
            raise forms.ValidationError("Your email must be only gmail")
        return data

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if not re.fullmatch(r'\+380\d{9}', data):
            raise forms.ValidationError("You phone must be entered in the format: '+380XXXXXXXXX'")
        return data
