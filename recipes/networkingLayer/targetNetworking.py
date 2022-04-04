from recipes.networkingLayer.baseRetailerNetworking import BaseRetailerNetworking
from recipes.networkingLayer.utils.networkingUtils import makeParams
from recipes.networkingLayer.networkingObjects.networkingObjects import PricingAndSourceData
import requests
import pydash

class TargetNetworking(BaseRetailerNetworking):
    def __init__(self) -> None:
        self.apiKey='3f015bca9bce7dbb2b377638fa5de0f229713c78'

    def getStoreData(self, lat, lon):
        params = makeParams(key=self.apiKey, place = lat + ',' + lon)
        response = requests.get('https://redsky.target.com/redsky_aggregations/v1/apps/nearby_stores_v1', params=params)
        return response.json()['data']['nearby_stores']['stores'][0]['store_id']

    def getProductInfo(self, upc, storeId, providedPrice):
        params = makeParams(key=self.apiKey, barcode=upc, pricing_store_id=storeId)
        response = requests.get('https://redsky.target.com/redsky_aggregations/v1/apps/product_from_barcode_v1', params=params)
        if response.status_code != 200:
            return PricingAndSourceData(price=providedPrice, useProvidedPrice=True)
        else:
            return PricingAndSourceData(price=str(pydash.get(response.json(), 'data.product_by_barcode.price.current_retail')))

    def getTaxonomy(self):
        pass