import hmac
from time import tzname
from rest_framework import generics
from rest_framework.response import Response

from datetime import datetime, timezone
import requests
import sys, os, base64, datetime, hashlib, hmac 
import requests # pip install requests
from recipes.networkingLayer import amazonNetworking, walmartNetworking
from recipes.networkingLayer import googleNetworking
from recipes.nondbmodels.amazonModels import ProfitabilityData
from recipes.serializers.amazonSerializers import AmazonProductSerializer 
from pprint import pprint

from scourgify import normalize_address_record


class AmazonList(generics.ListAPIView):

    def list(self, req, *args, **kwargs):
        # placeZipCodeResponse = googleNetworking.getAddressForPlace(placeId=self.request.query_params.get('placeId'))
        # address= normalize_address_record(placeZipCodeResponse.json()['result']['formatted_address'])
        # print("postal code = " + address['postal_code'])
        taxonomy = walmartNetworking.getTaxonomy()

        upcPriceDict = {}
        # for category in taxonomy['categories']:
        storeData = walmartNetworking.getStoreData(lat=self.request.query_params.get('lat') , lon=self.request.query_params.get('lon'))
        for item in walmartNetworking.getProductsByCategory("5428")['items']:
                productData = walmartNetworking.getProductInfo(upc=item['upc'], storeId=storeData[0]['no'])
                pprint(productData)
                error = productData.get('error', True)
                if error:
                        continue
                noInStorePrice = productData['data']['inStore']['price'].get('priceInCents', True)
                if noInStorePrice == True:
                        inStorePrice = "Not In Store"
                else:
                        inStorePrice = float(productData['data']['inStore']['price']['priceInCents']) / 100 
                upcPriceDict.update({item['upc']: inStorePrice})
        # pprint(storeData)

        # for upcs in productUpcs:
        #         productData = walmartNetworking.getProductInfo(upc=self.request.query_params.get('upc'), storeId=storeData[0]['no'])
        #         noInStorePrice = productData['data'].get('inStore', True)
        #         if noInStorePrice == True:
        #                 inStorePrice = "Not In Store"
        #         else:
        #                 inStorePrice = float(productData['data']['inStore']['price']['priceInCents']) / 100 
        #         upcPriceDict.update({})
        
        # pprint(productData)
        # inStorePrice = float(productData['data']['inStore']['price']['priceInCents']) / 100
        # print(inStorePrice)
        instructions = amazonNetworking.getPrepInstructions()
        amazonProductsList = []
        for upc, price in upcPriceDict:
                amazonProducts = amazonNetworking.getProducts(upc)['payload']['Items']
                # if len(amazonProducts) == 0:
                #         return Response({"Error": "UPC not found on Amazon"})

                
                for product in amazonProducts:
                        instructions = amazonNetworking.getPrepInstructions(product['Identifiers']['MarketplaceASIN']['ASIN'])
                        prices = amazonNetworking.getPrices(product['Identifiers']['MarketplaceASIN']['ASIN'])
                        fees = amazonNetworking.getFees(asin=product['Identifiers']['MarketplaceASIN']['ASIN'], price=prices['lowestPrice'])
                        restrictions = False if len(amazonNetworking.getRestrictions(asin=product['Identifiers']['MarketplaceASIN']['ASIN'])['restrictions']) == 0 else True
                        amazonProductsList.append(ProfitabilityData(asin=product['Identifiers']['MarketplaceASIN']['ASIN'], title=product['AttributeSets'][0]['Title'], imageUrl=product['AttributeSets'][0]['SmallImage']['URL'], salesRank=product['SalesRankings'][0]['Rank'], prices=prices, feeTotal=fees, restrictions=restrictions, retailPrice=price))

        return Response(AmazonProductSerializer(amazonProductsList, many=True).data)
        return Response(products)
        
