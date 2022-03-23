from django.db import models

from recipes.dbmodels.ingredientModel import Ingredient
# from recipes.dbmodels.ingredientRecipeUnitModel import IngredientRecipeUnit


class Recipe(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    servings =  models.SmallIntegerField()
    ingredients = models.ManyToManyField('IngredientRecipeUnit')

    class Meta:
        ordering = ['created']

    # def save(self, *args, **kwargs):
    #    # lexer = get_lexer_by_name(self.language)
    #     options = {'title': self.title} if self.title else {}
    #     super().save(*args, **kwargs)