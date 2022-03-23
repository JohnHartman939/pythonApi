from django.urls import path
from recipes.views.profitabilityView import ProfiabilityView
from recipes.views.amazonView import AmazonList
from recipes.views.ingredientRecipeUnitViews import IngredientRecipeUnitView
from recipes.views.recipeViews import RecipeView
from recipes.views.storeView import StoreList
from recipes.views.unitViews import UnitView
from recipes.views.ingredientViews import IngredientView

from rest_framework import routers

from recipes.views.visitView import VisitView

router = routers.DefaultRouter()

router.register(r'units', UnitView)
router.register(r'ingredients', IngredientView)
router.register(r'recipes', RecipeView)
router.register(r'visits', VisitView)
# router.register(r'stores', StoreList.as_view(), basename='stores')
# path('/stores', StoreList.as_view())

urlpatterns = router.urls

urlpatterns += [path('stores/', StoreList.as_view())]
urlpatterns += [path('amazon/', AmazonList.as_view())]
urlpatterns += [path('profitabilityChecker/', ProfiabilityView.as_view())]