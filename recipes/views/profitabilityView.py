from rest_framework import generics
from rest_framework.response import Response

from recipes.networkingLayer import amazonNetworking, walmartNetworking, googleNetworking, homeDepotNetworking
from recipes.nondbmodels.amazonModels import ProfitabilityData
from recipes.serializers.amazonSerializers import AmazonProductSerializer 
from pprint import pprint

from recipes.services.dataCollectionService import DataCollectionService



class ProfiabilityView(generics.ListAPIView):

    

    def list(self, req, *args, **kwargs):
        # placeZipCodeResponse = googleNetworking.getAddressForPlace(placeId=self.request.query_params.get('placeId'))
        # address= normalize_address_record(placeZipCodeResponse.json()['result']['formatted_address'])
        # print("postal code = " + address['postal_code'])
        # homeDepotNetworking.getProductDetails()
        
        dataCollector = DataCollectionService(self.request.query_params)
        dataCollector.getClosestStoreData()
        dataCollector.getInStoreProductData()
        dataCollector.getAmazonData()
        
        
        # upc=self.request.query_params.get('upc')
        # # for category in taxonomy['categories']:
        # storeData = walmartNetworking.getStoreData(lat=self.request.query_params.get('lat') , lon=self.request.query_params.get('lon'))
        # productData = walmartNetworking.getProductInfo(upc=upc, storeId=storeData[0]['no'])
        # pprint(productData)
        # if productData.get('error'):
        #     print('using provided price')
        #     inStorePrice = self.request.query_params.get('retailPrice')
        #     # return Response("error from walmart in store pricing")
        # elif not productData['data']['inStore']['price'].get('priceInCents'):
        #     inStorePrice = self.request.query_params.get('retailPrice')
        #     # return Response("not avilable in store")
        # else:
        #     print('using in store price')
        #     inStorePrice = float(productData['data']['inStore']['price']['priceInCents']) / 100 
        # # pprint(storeData)

        # # for upcs in productUpcs:
        # #         productData = walmartNetworking.getProductInfo(upc=self.request.query_params.get('upc'), storeId=storeData[0]['no'])
        # #         noInStorePrice = productData['data'].get('inStore', True)
        # #         if noInStorePrice == True:
        # #                 inStorePrice = "Not In Store"
        # #         else:
        # #                 inStorePrice = float(productData['data']['inStore']['price']['priceInCents']) / 100 
        # #         upcPriceDict.update({})
        
        # # pprint(productData)
        # # inStorePrice = float(productData['data']['inStore']['price']['priceInCents']) / 100
        # # print(inStorePrice)
        # amazonProductsList = []
        
        # amazonProducts = amazonNetworking.getProducts(upc)['payload']['Items']
        # if len(amazonProducts) == 0:
        #     return Response({"Error": "UPC not found on Amazon"})

                
        # for product in amazonProducts:
        #     instructions = amazonNetworking.getPrepInstructions(product['Identifiers']['MarketplaceASIN']['ASIN'])
        #     print('instructions\n')
        #     pprint(instructions.json())
        #     prices = amazonNetworking.getPrices(product['Identifiers']['MarketplaceASIN']['ASIN'])
        #     fees = amazonNetworking.getFees(asin=product['Identifiers']['MarketplaceASIN']['ASIN'], price=prices['lowestPrice'])
        #     restrictions = False if len(amazonNetworking.getRestrictions(asin=product['Identifiers']['MarketplaceASIN']['ASIN'])['restrictions']) == 0 else True
        #     amazonProductsList.append(ProfitabilityData(asin=product['Identifiers']['MarketplaceASIN']['ASIN'], title=product['AttributeSets'][0]['Title'], imageUrl=product['AttributeSets'][0]['SmallImage']['URL'], salesRank=product['SalesRankings'][0]['Rank'], prices=prices, feeTotal=fees, restrictions=restrictions, retailPrice=float(inStorePrice)))

        return Response(AmazonProductSerializer(dataCollector.amazonProductsList, many=True).data)
        
    def get_queryset(self):
        pass
        
