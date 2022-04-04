from pprint import pprint
from recipes.networkingLayer.amazonNetworking import AmazonNetworking
from recipes.networkingLayer.baseRetailerNetworking import BaseRetailerNetworking
from recipes.networkingLayer.otherNetworking import OtherNetworking
from recipes.networkingLayer.targetNetworking import TargetNetworking

from recipes.networkingLayer.walmartNetworking import WalmartNetworking
from datetime import date

from recipes.nondbmodels.amazonModels import ProfitabilityData


class DataCollectionService():
    def __init__(self, params) -> None:
        self.upc = params.get('upc')

        self.retailer = Retailer[params.get('retailer')] 
        self.amazon = AmazonNetworking()
        # self.retailer.testFunction("cool")

        # print(type(self.retailer) is WalmartNetworking)
        self.params = params
        self.amazonProduct = self.amazon.getProducts(self.upc)['payload']['Items'][0]
        if len(self.amazonProduct) == 0:
            raise UPCNotFoundException(upc=self.upc)
        self.asin = self.amazonProduct['Identifiers']['MarketplaceASIN']['ASIN']
        self.title = self.amazonProduct['AttributeSets'][0]['Title']
        self.imageUrl = self.amazonProduct['AttributeSets'][0]['SmallImage']['URL']
        self.salesRank = self.amazonProduct['SalesRankings'][0]['Rank']

    def getClosestStoreData(self):
        self.storeNumber = self.retailer.getStoreData(lat=self.params.get('lat') , lon=self.params.get('lon'))

    def getInStoreProductData(self):
        self.priceAndSource = self.retailer.getProductInfo(upc=self.upc, storeId=self.storeNumber, providedPrice=self.params.get('retailPrice'))

    def getAmazonData(self):
        self.amazonProductsList = []
        instructions = self.amazon.getPrepInstructions(self.asin).json()['payload']['ASINPrepInstructionsList'][0]
        # pprint(instructions)
        labelingRequirements = instructions['BarcodeInstruction']
        prepRequirements = instructions['PrepInstructionList']
        prices = self.amazon.getPrices(self.asin)
        # print(prices)
        fees = self.amazon.getFees(asin=self.asin, price=prices['lowestPrice'])
        restrictions = False if len(self.amazon.getRestrictions(asin=self.asin)['restrictions']) == 0 else True
        self.amazonProductsList.append(ProfitabilityData(asin=self.asin, 
            title=self.title, 
            imageUrl=self.imageUrl, 
            salesRank=self.salesRank, 
            prices=prices, 
            feeTotal=fees, 
            restrictions=restrictions, 
            retailPrice=float(self.priceAndSource.price), 
            priceUsedSource=self.priceAndSource.source,
            labeling=labelingRequirements,
            prep=prepRequirements))



Retailer = {
    'walmart': WalmartNetworking(),
    'target': TargetNetworking(),
    'other': OtherNetworking(),
}

class UPCNotFoundException(BaseException):
    def __init__(self, upc) -> None:
        self.errorCode = 404
        self.errorMessage = 'This UPC has not been found in the Amazon catalog'

