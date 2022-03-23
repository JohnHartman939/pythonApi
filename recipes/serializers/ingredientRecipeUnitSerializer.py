from rest_framework import serializers
from recipes.dbmodels.ingredientRecipeUnitModel import IngredientRecipeUnit

class IngredientRecipeUnitSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = IngredientRecipeUnit
        fields = ('ingredient', 'unit', 'quantity')