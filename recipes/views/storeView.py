from rest_framework.renderers import JSONRenderer
from rest_framework import generics
from rest_framework.response import Response
from recipes.nondbmodels import locationModel
from recipes.nondbmodels.locationModel import Location
from recipes.nondbmodels.storeModel import Store
from recipes.serializers.storeSerializer import StoreSerializer
from pprint import pprint
from recipes.networkingLayer import googleNetworking

import requests


class StoreList(generics.ListAPIView):

    def list(self, req, *args, **kwargs):

        stores = googleNetworking.getPlaces(location=self.request.query_params.get('location'))
        storeData = stores.json()['results']

        storeDataList = [ Store(store['name'], store['vicinity'], store['place_id'], Location(store['geometry']['location']['lat'],store['geometry']['location']['lng'])) for store in storeData ]
        pprint(stores.json())
        return Response(StoreSerializer(storeDataList, many=True).data)

class Params:

    def __init__(self, location, rankby ='distance', locationType = 'department_store', key = 'AIzaSyCbyfAxzRscrKMXVDIaNOkH1GDAP89eCIQ') -> None:
        self.data = {
            "location": location,
            "rankby" : rankby,
            "type" : locationType,
            "key" : key
        }

