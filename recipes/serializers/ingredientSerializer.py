from rest_framework import serializers
from recipes.dbmodels.ingredientModel import Ingredient

class IngredientSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Ingredient
        fields = ['url', 'name', 'created', 'recipes']
