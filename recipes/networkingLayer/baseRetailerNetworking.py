from abc import ABC, abstractclassmethod


class BaseRetailerNetworking(ABC):
    @abstractclassmethod
    def getStoreData(self, lat, lon):
        pass

    @abstractclassmethod
    def getProductInfo(self, upc, storeId, providedPrice):
        pass

    @abstractclassmethod
    def getTaxonomy(self):
        pass


 
