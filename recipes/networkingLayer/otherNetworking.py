from recipes.networkingLayer.baseRetailerNetworking import BaseRetailerNetworking
from recipes.networkingLayer.networkingObjects.networkingObjects import PricingAndSourceData


class OtherNetworking(BaseRetailerNetworking):
    def getStoreData(self, lat, lon):
        return "not applicable"

    def getProductInfo(self, upc, storeId, providedPrice):
        return PricingAndSourceData(price=providedPrice, useProvidedPrice=True)

    def getTaxonomy(self):
        pass