from rest_framework import serializers

class LocationSerializer(serializers.Serializer):
    lat = serializers.CharField()
    lon = serializers.CharField()
