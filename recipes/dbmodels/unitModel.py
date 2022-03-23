from django.db import models

from recipes.dbmodels.recipeModel import Recipe

class Unit(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=20)
    recipes = models.ManyToManyField(Recipe, through='IngredientRecipeUnit')