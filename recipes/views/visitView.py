from recipes.dbmodels.visitModel import Visit
from recipes.serializers.visitSerializer import VisitSerializer
from rest_framework import viewsets

class VisitView(viewsets.ModelViewSet):
    """
    Retrieve, update or delete a snippet instance.
    """
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer