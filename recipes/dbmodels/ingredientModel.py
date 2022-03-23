from django.db import models


class Ingredient(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    recipes = models.ManyToManyField('Recipe', through='IngredientRecipeUnit')
