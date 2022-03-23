from rest_framework import serializers

from recipes.dbmodels.unitModel import Unit

class UnitSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Unit
        fields = ['url', 'name', 'created', 'recipes']