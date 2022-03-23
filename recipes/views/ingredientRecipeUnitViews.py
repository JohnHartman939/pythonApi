from rest_framework import viewsets

from recipes.dbmodels.ingredientRecipeUnitModel import IngredientRecipeUnit
from recipes.serializers.ingredientRecipeUnitSerializer import IngredientRecipeUnitSerializer

class IngredientRecipeUnitView(viewsets.ModelViewSet):
    queryset = IngredientRecipeUnit.objects.all()
    serializer_class = IngredientRecipeUnitSerializer