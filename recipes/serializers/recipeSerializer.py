from rest_framework import serializers
from recipes.dbmodels.recipeModel import Recipe
from recipes.serializers.ingredientRecipeUnitSerializer import IngredientRecipeUnitSerializer
from recipes.dbmodels.ingredientRecipeUnitModel import IngredientRecipeUnit

class RecipeSerializer(serializers.HyperlinkedModelSerializer):

    ingredients = IngredientRecipeUnitSerializer(source='recipes', many=True)

    class Meta:
        model = Recipe
        fields = ['url', 'title', 'servings', 'ingredients']

    def create(self, validated_data):
        print(validated_data)
        ingredientsData = validated_data.pop('recipes')
        recipe = Recipe.objects.create(**validated_data)
        for ingredientData in ingredientsData:
            IngredientRecipeUnit.objects.create(recipes=recipe, **ingredientData)
        return recipe