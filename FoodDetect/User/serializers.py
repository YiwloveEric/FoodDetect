from rest_framework import serializers
from User.models import Favorites


class ReviewFavorViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'
