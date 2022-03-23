from recipes.dbmodels.recipeModel import Recipe
from recipes.serializers.recipeSerializer import RecipeSerializer
from rest_framework import viewsets

class RecipeView(viewsets.ModelViewSet):
    """
    Retrieve, update or delete a snippet instance.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer