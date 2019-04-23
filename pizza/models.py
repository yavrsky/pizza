from django.db import models

# Create your models here.
class Ingredient(models.Model):
    INPUT_TYPE = (
        ('num','Number'),
        ('rad', 'Radio')
    )

    title = models.CharField(max_length=25)
    type = models.CharField(max_length=3, choices=INPUT_TYPE)

    def __str__(self):
        return self.title



class Component(models.Model):
    name = models.CharField(max_length=25)
    price = models.FloatField(default=0)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
