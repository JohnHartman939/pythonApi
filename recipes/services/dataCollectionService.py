from enum import Enum
from pprint import pprint
from recipes.networkingLayer import amazonNetworking
from recipes.networkingLayer.baseRetailerNetworking import BaseRetailerNetworking

from recipes.networkingLayer.walmartNetworking import WalmartNetworking
from datetime import date

from recipes.nondbmodels.amazonModels import ProfitabilityData


class DataCollectionService():
    def __init__(self, params) -> None:
        self.upc = params.get('upc')

        self.retailer = Retailer[params.get('retailer')] 
        self.retailer.testFunction("cool")

        print(type(self.retailer) is WalmartNetworking)
        self.params = params
        self.amazonProduct = amazonNetworking.getProducts(self.upc)['payload']['Items'][0]
        if len(self.amazonProduct) == 0:
            raise UPCNotFoundException(upc=self.upc)
        self.asin = self.amazonProduct['Identifiers']['MarketplaceASIN']['ASIN']
        self.title = self.amazonProduct['AttributeSets'][0]['Title']
        self.imageUrl = self.amazonProduct['AttributeSets'][0]['SmallImage']['URL']
        self.salesRank = self.amazonProduct['SalesRankings'][0]['Rank']

    def getClosestStoreData(self):
        self.storeNumber = self.retailer.getStoreData(lat=self.params.get('lat') , lon=self.params.get('lon'))[0]['no']

    def getInStoreProductData(self):
        self.inStoreProductData = self.retailer.getProductInfo(upc=self.upc, storeId=self.storeNumber)
        pprint(self.inStoreProductData)
        if self.inStoreProductData.get('error'):
            self.priceUsedSource = 'using provided price'
            self.inStorePrice = self.params.get('retailPrice')
            # return Response("error from walmart in store pricing")
        elif not self.inStoreProductData['data']['inStore']['price'].get('priceInCents'):
            self.priceUsedSource = 'using provided price, not found in store'
            self.inStorePrice = self.params.get('retailPrice')
            # return Response("not avilable in store")
        else:
            self.priceUsedSource = 'using price from retailer API'
            self.inStorePrice = float(self.inStoreProductData['data']['inStore']['price']['priceInCents']) / 100 

    def getAmazonData(self):
        self.amazonProductsList = []
        instructions = amazonNetworking.getPrepInstructions(self.asin)
        print('instructions\n')
        print(instructions.json())
        prices = amazonNetworking.getPrices(self.asin)
        print(prices)
        fees = amazonNetworking.getFees(asin=self.asin, price=prices['lowestPrice'])
        restrictions = False if len(amazonNetworking.getRestrictions(asin=self.asin)['restrictions']) == 0 else True
        self.amazonProductsList.append(ProfitabilityData(asin=self.asin, 
            title=self.title, 
            imageUrl=self.imageUrl, 
            salesRank=self.salesRank, 
            prices=prices, 
            feeTotal=fees, 
            restrictions=restrictions, 
            retailPrice=float(self.inStorePrice), 
            priceUsedSource=self.priceUsedSource))

# class Retailer(Enum):
#     walmart = WalmartNetworking()

Retailer: dict[str, BaseRetailerNetworking] = {
    'walmart': WalmartNetworking()
}

class UPCNotFoundException(BaseException):
    def __init__(self, upc) -> None:
        self.errorCode = 404
        self.errorMessage = 'This UPC has not been found in the Amazon catalog'
