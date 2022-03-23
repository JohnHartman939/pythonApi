
# import hashlib
# import hmac
# from pprint import pprint
# import requests
# from time import time


# privateKey = 'MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDGYIMokYn//ULdCAh8+mBRPNTFKWgQOtApBjumIohokj/j92Ityu//NFGQGSgZP44b+OyulK8rX6XVlXGPsaNxgf7/ar3p+1GSEXk4ejlgMUfGejtvhK2LuNcqnby2yZ5WsEGR6swdzNAugbVsifxnGSGrnne6IuHPfbAomlY4yjO6wxH1/bcrX0efIk0VJ/MZvenWVmLXdCKgamCl95gh4XsVn6htPpYOZZLFhC+HjDCHRitGEFd2N231RD05CkE8E5pa25pQVeFbMe0t4Fs0oVFf2Cn5KM8yAsaR7s+YWB2o3YmkZbdACKr5k35rzMpI17iSVPvfh9JPdFqADkNAgMBAAECggEAYZXyj09g8nO0o6SjAE/ud6gUBtVCotE7uyKczzInpkFjepIkUuCExScIhHlLl3gDQVFnpM3xicWof3PfhE9fVqQbO6xXtjVyQAemeRjvBpnXdBSHDmnXMWeBOS6VOdnesUhNSLvTv6izpsCcQh08twc3EGXd/8CneqUJsGN0rUtaNLEWwm06YhrMu77wqOR9Qwf+VAC/IvcQfBiDd657MgGL4tUn01/a0gM5YJK9sbVxHZrFXNY7cMT3MmWxNDqukKtnlIZo07tu3NHpv9j4juTcNAajOMUxQ1cfrQ5u7F/ChfcNCjQTPW4Jvpc1qvrscUcAZ23eO7C0mJYk0XmwIQKBgQD/0I5/bi/GkDt1DNMtHAKBbJenT60aKrK2H9boXmKORgaxZNBIeGcIm3ghYkbJdN/Vae0oeEYo9d9I1isxXjf6mb8B4XuTcEqs8r7hGZKpChv3LtC+HuTo7bI++A4eKQMkWAAzB0c3jAj71wVxVX2h4MGjEf37BD1ySfPoe745FQKBgQDGhU2mXhWCe23XEhGyfbbcaiufHTqPP1TtXisadPESUjGA5ydYyVf+4171DMvEPL5s+vr1ULg0245yLYOSFojWxD1f8EkhOQLXtLLyUglDlgXFRv6emezaO/X8ok68a0HU8MSKpmR+Ylp05DpkIcVfSVreEwaXcIWTK/kaKHeOGQKBgHYon9kuTPT7Y+sxzEz2thWP0hCe1cbTWA6VcE+OYRl0MN05QpdmvbiVDwzkduvQhx7tOXTK8SU0RDlBa1v3OAYRg89blhfI80UlLpOMm1hm6fnnbtWSMYuBVyaMrwCxUtkzqIvpXbTDgtbIP6RUp53g0a//vH94OuWSUQ3eMkPtAoGBALUcvIDBaQJHtSf3limvQ3rHadCaC+jQMJz1woE6mwzJ69vcByubVSp3KRSLfgMkH96xAu93mvauL8C/AT/wSxsUoaG7SByFNLCybGdirIz6e31FjdoIN+vJtFutgAOqHr80gTq1Hw2mkTv/U74yiSyrcbkUxni28UYZYgOZU6lRAoGAa68eQb1+B1ZGxddlS5P6bFkmjEi8o/mfRxHLJ58g1BowX8lUwE2KFNv11gE7xhYJLwBrD5mPCDrICzFkplwApc7m1728A1FiIxhVyUKZGUeEJD418eKE1cdp0cJLHE4S7AqcOXQPmbdSGgXUVqAwcYp3sVTyhulEo6h3J/oo3es='

# def getOAuthToken():
#     headers = Headers()
#     oAuthResponse = requests.get('https://developer.api.walmart.com/api-proxy/service/affil/product/v2/stores', headers=headers.headersDict)
#     pprint(oAuthResponse.json())

# class Headers():
#     def __init__(self, **kwargs) -> None:
#         self.headersDict = {'WM_SEC.KEY_VERSION':'2',
#             'WM_CONSUMER.ID':'af4e9a3b-1bce-4ac7-b8b7-f06eb3f69d0a',
#             'WM_CONSUMER.INTIMESTAMP': str(round(time()*1000)) }
#         self.headerKeysString = ''
#         self.headerValuesString = ''
#         for key,value in sorted (self.headersDict.items()):
#             # self.headersDict.update({key: value})
#             self.headerKeysString = self.headerKeysString + key + ';'
#             self.headerValuesString = self.headerValuesString + value + '\n'
#         # print(self.headersDict)
#         # print(self.headerKeysString)
#         self.headersDict.update({'WM_SEC.AUTH_SIGNATURE': self.sign(self.headerValuesString)})
#         print(self.headersDict)



#     def sign(self, stringToSign):
#         return hmac.new(bytes(privateKey, encoding='utf-8'), bytes(stringToSign, encoding='utf-8'), hashlib.sha256).hexdigest()

import requests, time
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import base64
import os

from recipes.networkingLayer.baseRetailerNetworking import BaseRetailerNetworking

class WalmartNetworking(BaseRetailerNetworking):


    def __init__(self) -> None:
        self.consumerId = os.environ['WALMART_CONSUMER_ID']
        self.keyVersion = '2'
        self.epochTime = str(int(time.time()*1000))

    def _sign(self):
        sortedHashString = self.consumerId +'\n'+ self.epochTime +'\n'+ self.keyVersion +'\n'
        encodedHashString = sortedHashString.encode()
        try:
            with open('./recipesInPython/WM_IO_private_key.pem', 'r') as f:
                key = RSA.importKey(f.read())
                print(key)
        except IOError as e:
            print(e)

        hasher = SHA256.new(encodedHashString)
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(hasher)
        return str(base64.b64encode(signature),'utf-8')



    def getStoreData(self, lat, lon):
        params = Params(lat=lat, lon=lon)
        headers = { 'WM_CONSUMER.ID' : self.consumerId,
                'WM_CONSUMER.INTIMESTAMP' : self.epochTime,
                'WM_SEC.AUTH_SIGNATURE' : self._sign(),
                'WM_SEC.KEY_VERSION' : self.keyVersion
                }
        response = requests.get('https://developer.api.walmart.com/api-proxy/service/affil/product/v2/stores', headers=headers, params=params.data)
        return response.json()

    def getProductInfo(self, upc, storeId):
        productInfo = requests.get('https://search.mobile.walmart.com/v1/products-by-code/UPC/{}'.format(upc), headers={'Accept': 'Application/json', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}, params={'storeId': storeId})
        print(productInfo.url)
        return productInfo.json()

    def getTaxonomy(self):
        headers = { 'WM_CONSUMER.ID' : self.consumerId,
                'WM_CONSUMER.INTIMESTAMP' : self.epochTime,
                'WM_SEC.AUTH_SIGNATURE' : self._sign(),
                'WM_SEC.KEY_VERSION' : self.keyVersion
                }
        response = requests.get('https://developer.api.walmart.com/api-proxy/service/affil/product/v2/taxonomy', headers=headers)
        return response.json()

    def getProductsByCategory(self, catalogId):
        params = Params(category=catalogId, count='1')
        headers = { 'WM_CONSUMER.ID' : self.consumerId,
                'WM_CONSUMER.INTIMESTAMP' : self.epochTime,
                'WM_SEC.AUTH_SIGNATURE' : self._sign(),
                'WM_SEC.KEY_VERSION' : self.keyVersion
                }
        response = requests.get('https://developer.api.walmart.com/api-proxy/service/affil/product/v2/paginated/items', headers=headers)
        return response.json()

    def getoauthToken(self):
        headers = { 'WM_CONSUMER.ID' : self.consumerId,
            'WM_CONSUMER.INTIMESTAMP' : self.epochTime,
            'WM_SEC.AUTH_SIGNATURE' : self._sign(),
            'WM_SEC.KEY_VERSION' : self.keyVersion
                }
        tokenResponse = requests.post('https://developer.api.walmart.com/api-proxy/service', headers=headers)

    def testFunction(self, testString):
        print(testString)

class Params:
    def __init__(self, **kwargs) -> None:
        self.data = {}
        for key, value in kwargs.items():
            self.data.update({key:value})

    