from django.contrib import admin

from .models import Ingredient, Component
# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Component)
