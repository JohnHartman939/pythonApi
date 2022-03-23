from rest_framework import viewsets

from recipes.dbmodels.unitModel import Unit
from recipes.serializers.unitSerializer import UnitSerializer

class UnitView(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer