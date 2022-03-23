from rest_framework import viewsets

from recipes.dbmodels.ingredientModel import Ingredient
from recipes.serializers.ingredientSerializer import IngredientSerializer

class IngredientView(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer