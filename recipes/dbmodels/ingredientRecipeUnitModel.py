from django.db import models
from recipes.dbmodels.ingredientModel import Ingredient

from recipes.dbmodels.recipeModel import Recipe
from recipes.dbmodels.unitModel import Unit

class IngredientRecipeUnit(models.Model):
    recipes = models.ForeignKey(Recipe, related_name='recipes', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, related_name='ingredients',on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.ForeignKey(Unit, related_name='units',on_delete=models.CASCADE)