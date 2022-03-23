from django.db import models

class Visit(models.Model):
    dateTimeOfVisit = models.DateTimeField(auto_now_add=True)
    storeName = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    lat = models.CharField(max_length=50)
    lon = models.CharField(max_length=50)
    placeId = models.CharField(max_length=50)
    

