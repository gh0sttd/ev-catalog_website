from rest_framework import serializers
from .models import Car, Favorite

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    car_details = CarSerializer(source='car', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'car', 'added_at', 'car_details']
