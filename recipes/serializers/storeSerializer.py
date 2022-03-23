from rest_framework import serializers

from recipes.serializers.locationSerializer import LocationSerializer

class StoreSerializer(serializers.Serializer):
    storeName = serializers.CharField()
    address = serializers.CharField()
    placeId = serializers.CharField()
    location = LocationSerializer()
