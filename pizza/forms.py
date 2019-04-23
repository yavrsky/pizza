from django.forms import ModelForm, Form
from django import forms
from .models import *


class ComponentForm(forms.Form):
    number = forms.DecimalField(min_value=0, label='')

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
