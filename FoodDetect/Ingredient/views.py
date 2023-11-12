from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Ingredient
from .serializers import IngredientSerializer


# Create your views here.

class IngredientView(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


