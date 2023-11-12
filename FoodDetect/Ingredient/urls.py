from django.urls import path, include
from .views import IngredientView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Ingredient', IngredientView, basename='Ingredient')
urlpatterns = [

]
urlpatterns += router.urls
