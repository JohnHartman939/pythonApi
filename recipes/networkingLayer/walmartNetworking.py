import requests, time
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import base64
import os
import environ
import pydash

from recipes.networkingLayer.networkingObjects.networkingObjects import PricingAndSourceData


env = environ.Env()
from pprint import pprint
from recipes.networkingLayer.baseRetailerNetworking import BaseRetailerNetworking
from recipes.networkingLayer.utils.networkingUtils import makeParams

class WalmartNetworking(BaseRetailerNetworking):


    def __init__(self) -> None:
        self.consumerId = os.environ['WALMART_CONSUMER_ID']
        self.keyVersion = '2'


    def _sign(self):
        epochTime = str(int(time.time()*1000))
        sortedHashString = self.consumerId +'\n'+ epochTime +'\n'+ self.keyVersion +'\n'
        encodedHashString = sortedHashString.encode()
        key = RSA.importKey(env.str('WALMART_CERT', multiline=True))
        hasher = SHA256.new(encodedHashString)
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(hasher)
        return str(base64.b64encode(signature),'utf-8')



    def getStoreData(self, lat, lon):
        params = makeParams(lat=lat, lon=lon)
        epochTime = str(int(time.time()*1000))
        headers = { 'WM_CONSUMER.ID' : self.consumerId,
                'WM_CONSUMER.INTIMESTAMP' : epochTime,
                'WM_SEC.AUTH_SIGNATURE' : self._sign(),
                'WM_SEC.KEY_VERSION' : self.keyVersion
                }
        response = requests.get('https://developer.api.walmart.com/api-proxy/service/affil/product/v2/stores', headers=headers, params=params)
        # pprint(response.json())
        return response.json()[0]['no']

    def getProductInfo(self, upc, storeId, providedPrice):
        params = makeParams(storeId=storeId)
        productInfo = requests.get('https://search.mobile.walmart.com/v1/products-by-code/UPC/{}'.format(upc), headers={'Accept': 'Application/json', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}, params=params)
        print(productInfo.url)
        if productInfo.status_code != 200:
            return PricingAndSourceData(price=str(providedPrice), useProvidedPrice=True)
        else:
            return PricingAndSourceData(price=str(pydash.get(productInfo.json(), 'data.inStore.price.priceInCents') /100))

    def getTaxonomy(self):
        epochTime = str(int(time.time()*1000))
        headers = { 'WM_CONSUMER.ID' : self.consumerId,
                'WM_CONSUMER.INTIMESTAMP' : epochTime,
                'WM_SEC.AUTH_SIGNATURE' : self._sign(),
                'WM_SEC.KEY_VERSION' : self.keyVersion
                }
        response = requests.get('https://developer.api.walmart.com/api-proxy/service/affil/product/v2/taxonomy', headers=headers)
        return response.json()

    def getProductsByCategory(self, catalogId):
        epochTime = str(int(time.time()*1000))
        params = makeParams(category=catalogId, count='1')
        headers = { 'WM_CONSUMER.ID' : self.consumerId,
                'WM_CONSUMER.INTIMESTAMP' : epochTime,
                'WM_SEC.AUTH_SIGNATURE' : self._sign(),
                'WM_SEC.KEY_VERSION' : self.keyVersion
                }
        response = requests.get('https://developer.api.walmart.com/api-proxy/service/affil/product/v2/paginated/items', headers=headers, params=params)
        return response.json()

    def getoauthToken(self):
        epochTime = str(int(time.time()*1000))
        headers = { 'WM_CONSUMER.ID' : self.consumerId,
            'WM_CONSUMER.INTIMESTAMP' : epochTime,
            'WM_SEC.AUTH_SIGNATURE' : self._sign(),
            'WM_SEC.KEY_VERSION' : self.keyVersion
                }
        tokenResponse = requests.post('https://developer.api.walmart.com/api-proxy/service', headers=headers)

    def testFunction(self, testString):
        print(testString)



    