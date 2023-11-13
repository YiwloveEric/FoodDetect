from rest_framework import serializers
from .models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientOcrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'ingredient_id', 'chinese_name', 'english_name', 'introduction', 'effects', 'rating',
            'potential_risk_people',
            'daily_intake_recommendation')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        res = {
            "scores": data['rating'],
            "arr": data['chinese_name'],
        }
        return {
            'id': data['ingredient_id'],
            'res': res
        }