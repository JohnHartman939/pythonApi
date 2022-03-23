from rest_framework import serializers
from recipes.dbmodels.visitModel import Visit

class VisitSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Visit
        fields = ['url', 'storeName', 'address', 'lat', 'lon', 'placeId', 'dateTimeOfVisit']
# arn:aws:iam::520395113210:role/pythonSellerApiRole

# Atzr|IwEBIB3KavV-4w2mplqlWsHdb2x4EprNZAzSYwCADMm53Iz89Ic_BG-VE3qfcMdblQWsWpOd91wqzYqQsvejZTp2BEwqA7683FxaP4XySrT8HyTLJfcnYENJqtrpQXIk27MDCtfkduDtSPxVh9yfflP_fd-41KnyZur0gORa5OytyARNtQu1UGzA51np9xtIMoAhMqD6P9Aez6CIaYu5oBWZTEMToYD5-aneDRX3Vrvp5_vCrE5bDWUNhu6B_MRcybBaHuTo3SfAX2w-upvQMx3ZXXTsmphNUFdLZexrg9XcU6I3eJzCd-5XVmatdE_TQord0SI