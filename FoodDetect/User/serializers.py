from rest_framework import serializers
from User.models import Favorites, Users


class ReviewFavorViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
