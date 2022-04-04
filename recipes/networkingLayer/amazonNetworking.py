from datetime import datetime, timedelta, timezone
from functools import wraps
import hashlib
import hmac
import requests
import boto3
import boto3.session
from difflib import Differ, SequenceMatcher
from rest_framework.parsers import JSONParser
import io

import os
from pprint import pprint

from recipes.serializers.amazonSerializers import AmazonPriceSummarySerializer

class AmazonTokenManager():

    def __init__(self) -> None:
        self.getAccessToken()

    def getAccessToken(self):
            awsSession = boto3.session.Session(aws_access_key_id=os.environ['AWS_ACCESS_KEY'], aws_secret_access_key=os.environ['AWS_SECRET_KEY'], region_name='us-east-1')

        # print(awsSession.get_available_services())

            stsClient = awsSession.client(service_name='sts')

            stsResponse = stsClient.assume_role(RoleArn=os.environ['AWS_ARN'], RoleSessionName='erniesSession')

        # print(stsResponse)
            self.tokenExipirationTime = stsResponse['Credentials']['Expiration']
            print(self.tokenExipirationTime)
            self.spAccessKeyId = stsResponse['Credentials']['AccessKeyId']
        # print('\nAccess Key = ' + spAccessKeyId)
            self.spSecretAccessKey = stsResponse['Credentials']['SecretAccessKey']
        # print('\nSecret Access Key = ' + spSecretAccessKey)

            self.spSecurityToken = stsResponse['Credentials']['SessionToken']
        # print(stsResponse)

            accessTokenRequest = requests.post('https://api.amazon.com/auth/o2/token', params={
                    "grant_type": "refresh_token",
                    "refresh_token": os.environ['SELLER_CENTRAL_APP_REFRESH_TOKEN'],
                    "client_id": os.environ['SELLER_CENTRAL_APP_CLIENT_ID'],
                    "client_secret": os.environ['SELLER_CENTRAL_APP_CLIENT_SECRET']
                })
            self.accessToken = accessTokenRequest.json()['access_token']

            print('access token = ' + self.accessToken)
class AmazonNetworking():
    tokenManager = AmazonTokenManager()

    def __init__(self):
        
        # tokenManager.getAccessToken()
        # self.getAccessToken()
        self.amzUserAgent = 'pythonApi/0.0 (Language=Python)'
        self.endpoint = 'https://sellingpartnerapi-na.amazon.com'
        self.service = 'execute-api'
        self.host = 'sellingpartnerapi-na.amazon.com'
        self.region = 'us-east-1'
    # def log_real_decorator(f):
    #     @wraps(f)
    #     def wrapper(self, *args, **kw):      
    #         print "I am the decorator, I know that self is", self, "and I can do whatever I want with it!"
    #         print "I also got other args:", args, kw           
    #         f(self, *args, **kw)
    #     # ^ pass on self here

    #     return wrapper

    def checkExpiration(func):
        @wraps(func)
        def wrapper(self, *args, **kw):
            if datetime.now(timezone.utc) - timedelta(seconds=30) > self.tokenManager.tokenExipirationTime:
                self.tokenManager.getAccessToken()
            return func(self, *args , **kw)
        return wrapper


    # def getAccessToken(self):
    #     awsSession = boto3.session.Session(aws_access_key_id=os.environ['AWS_ACCESS_KEY'], aws_secret_access_key=os.environ['AWS_SECRET_KEY'], region_name='us-east-1')

    # # print(awsSession.get_available_services())

    #     stsClient = awsSession.client(service_name='sts')

    #     stsResponse = stsClient.assume_role(RoleArn=os.environ['AWS_ARN'], RoleSessionName='erniesSession')

    # # print(stsResponse)
    #     self.tokenExipirationTime = stsResponse['Credentials']['Expiration']
    #     print(self.tokenExipirationTime)
    #     self.spAccessKeyId = stsResponse['Credentials']['AccessKeyId']
    # # print('\nAccess Key = ' + spAccessKeyId)
    #     self.spSecretAccessKey = stsResponse['Credentials']['SecretAccessKey']
    # # print('\nSecret Access Key = ' + spSecretAccessKey)

    #     self.spSecurityToken = stsResponse['Credentials']['SessionToken']
    # # print(stsResponse)

    #     accessTokenRequest = requests.post('https://api.amazon.com/auth/o2/token', params={
    #             "grant_type": "refresh_token",
    #             "refresh_token": os.environ['SELLER_CENTRAL_APP_REFRESH_TOKEN'],
    #             "client_id": os.environ['SELLER_CENTRAL_APP_CLIENT_ID'],
    #             "client_secret": os.environ['SELLER_CENTRAL_APP_CLIENT_SECRET']
    #         })
    #     self.accessToken = accessTokenRequest.json()['access_token']
    #     self.amzUserAgent = 'pythonApi/0.0 (Language=Python)'
    #     self.endpoint = 'https://sellingpartnerapi-na.amazon.com'
    #     self.service = 'execute-api'
    #     self.host = 'sellingpartnerapi-na.amazon.com'
    #     self.region = 'us-east-1'
    #     print('access token = ' + self.accessToken)

    def __sign(self, key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    def __getSignatureKey(self, key, dateStamp, regionName, serviceName):
        kDate = self.__sign(('AWS4' + key).encode('utf-8'), dateStamp)
        kRegion = self.__sign(kDate, regionName)
        kService = self.__sign(kRegion, serviceName)
        kSigning = self.__sign(kService, 'aws4_request')
        return kSigning

    @checkExpiration
    def getProducts(self, upc=None):
        # orderDate = datetime.datetime(2007, 3, 6, 15, 29, 43, 79060, tzinfo=datetime.timezone.utc).
        # print('upc=' + upc)
        method = 'GET'

        
        # request_parameters = 'CreatedAfter=2022-03-10&MarketplaceIds=ATVPDKIKX0DER'
        # request_parameters = 'MarketplaceId=ATVPDKIKX0DER&Query=' + upc
        request_parameters = 'MarketplaceId=ATVPDKIKX0DER&UPC=' + upc
        
    # Key derivation functions. See:
    # http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python


    # Read AWS access key from env. variables or configuration file. Best practice is NOT
    # to embed credentials in code.


    # Create a date for headers and the credential string
        t = datetime.now(timezone.utc)
        amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope
        # print(amzdate)


    # ************* TASK 1: CREATE A CANONICAL REQUEST *************
    # http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html

    # Step 1 is to define the verb (GET, POST, etc.)--already done.

    # Step 2: Create canonical URI--the part of the URI from domain to query 
    # string (use '/' if no path)
        canonical_uri = '/catalog/v0/items' 
        # canonical_uri = '/orders/v0/orders'

    # Step 3: Create the canonical query string. In this example (a GET request),
    # request parameters are in the query string. Query string values must
    # be URL-encoded (space=%20). The parameters must be sorted by name.
    # For this example, the query string is pre-formatted in the request_parameters variable.
        canonical_querystring = request_parameters

    # Step 4: Create the canonical headers and signed headers. Header names
    # must be trimmed and lowercase, and sorted in code point order from
    # low to high. Note that there is a trailing \n.
        canonical_headers = 'host:' + self.host + '\n' + 'user-agent:' + self.amzUserAgent + '\n' + 'x-amz-access-token:' + self.tokenManager.accessToken + '\n' + 'x-amz-date:' + amzdate + '\n' + 'x-amz-security-token:' + self.tokenManager.spSecurityToken + '\n'

    # Step 5: Create the list of signed headers. This lists the headers
    # in the canonical_headers list, delimited with ";" and in alpha order.
    # Note: The request can include any headers; canonical_headers and
    # signed_headers lists those that you want to be included in the 
    # hash of the request. "Host" and "x-amz-date" are always required.
        signed_headers = 'host;user-agent;x-amz-access-token;x-amz-date;x-amz-security-token'

    # Step 6: Create payload hash (hash of the request body content). For GET
    # requests, the payload is an empty string ("").
        payload_hash = hashlib.sha256(('').encode('utf-8')).hexdigest()

    # Step 7: Combine elements to create canonical request
        canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
        # print('\nCanonical String\n' + canonical_request + '\n')

    # ************* TASK 2: CREATE THE STRING TO SIGN*************
    # Match the algorithm to the hashing algorithm you use, either SHA-1 or
    # SHA-256 (recommended)
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = datestamp + '/' + self.region + '/' + self.service + '/' + 'aws4_request'
        string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

        # print('\nstring to sign\n' + string_to_sign + '\n')
    # ************* TASK 3: CALCULATE THE SIGNATURE *************
    # Create the signing key using the function defined above.
        signing_key = self.__getSignatureKey(self.tokenManager.spSecretAccessKey, datestamp, self.region, self.service)

    # Sign the string_to_sign using the signing_key
        signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()


    # ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
    # The signing information can be either in a query string value or in 
    # a header named Authorization. This code shows how to use a header.
    # Create authorization header and add to request headers
        authorization_header = algorithm + ' ' + 'Credential=' + self.tokenManager.spAccessKeyId + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

    # The request can include any headers, but MUST include "host", "x-amz-date", 
    # and (for this scenario) "Authorization". "host" and "x-amz-date" must
    # be included in the canonical_headers and signed_headers, as noted
    # earlier. Order here is not significant.
    # Python note: The 'host' header is added automatically by the Python 'requests' library.
        headers = {'user-agent' : self.amzUserAgent, 'x-amz-date':amzdate, 'x-amz-access-token': self.tokenManager.accessToken, 'x-amz-security-token': self.tokenManager.spSecurityToken, 'Authorization':authorization_header}


    # ************* SEND THE REQUEST *************
        request_url = self.endpoint + canonical_uri + '?' + canonical_querystring


        r = requests.get(request_url, headers=headers)
        return r.json()


    def getRestrictions(self, asin):
        method = 'GET'
        request_parameters = 'asin=' + asin + '&conditionType=new_new&marketplaceIds=ATVPDKIKX0DER&sellerId=A2WJDCPTZ40M4Q'
        t = datetime.utcnow()
        amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        datestamp = t.strftime('%Y%m%d')
        canonical_uri = '/listings/2021-08-01/restrictions'
        canonical_querystring = request_parameters
        canonical_headers = 'host:' + self.host + '\n' + 'user-agent:' + self.amzUserAgent + '\n' + 'x-amz-access-token:' + self.tokenManager.accessToken + '\n' + 'x-amz-date:' + amzdate + '\n' + 'x-amz-security-token:' + self.tokenManager.spSecurityToken + '\n'
        signed_headers = 'host;user-agent;x-amz-access-token;x-amz-date;x-amz-security-token'
        payload_hash = hashlib.sha256(('').encode('utf-8')).hexdigest()
        canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = datestamp + '/' + self.region + '/' + self.service + '/' + 'aws4_request'
        string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
        signing_key = self.__getSignatureKey(self.tokenManager.spSecretAccessKey, datestamp, self.region, self.service)
        signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
        authorization_header = algorithm + ' ' + 'Credential=' + self.tokenManager.spAccessKeyId + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
        headers = {'user-agent' : self.amzUserAgent, 'x-amz-date':amzdate, 'x-amz-access-token': self.tokenManager.accessToken, 'x-amz-security-token': self.tokenManager.spSecurityToken, 'Authorization':authorization_header}
        request_url = self.endpoint + canonical_uri + '?' + canonical_querystring
        r = requests.get(request_url, headers=headers)
        return r.json()

    def getRestrictions(self, asin):
        method = 'GET'
        request_parameters = 'asin=' + asin + '&conditionType=new_new&marketplaceIds=ATVPDKIKX0DER&sellerId=' + os.environ['SELLER_CENTRAL_SELLER_ID']
        t = datetime.utcnow()
        amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        datestamp = t.strftime('%Y%m%d')
        canonical_uri = '/listings/2021-08-01/restrictions'
        canonical_querystring = request_parameters
        canonical_headers = 'host:' + self.host + '\n' + 'user-agent:' + self.amzUserAgent + '\n' + 'x-amz-access-token:' + self.tokenManager.accessToken + '\n' + 'x-amz-date:' + amzdate + '\n' + 'x-amz-security-token:' + self.tokenManager.spSecurityToken + '\n'
        signed_headers = 'host;user-agent;x-amz-access-token;x-amz-date;x-amz-security-token'
        payload_hash = hashlib.sha256(('').encode('utf-8')).hexdigest()
        canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = datestamp + '/' + self.region + '/' + self.service + '/' + 'aws4_request'
        string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
        signing_key = self.__getSignatureKey(self.tokenManager.spSecretAccessKey, datestamp, self.region, self.service)
        signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
        authorization_header = algorithm + ' ' + 'Credential=' + self.tokenManager.spAccessKeyId + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
        headers = {'user-agent' : self.amzUserAgent, 'x-amz-date':amzdate, 'x-amz-access-token': self.tokenManager.accessToken, 'x-amz-security-token': self.tokenManager.spSecurityToken, 'Authorization':authorization_header}
        request_url = self.endpoint + canonical_uri + '?' + canonical_querystring
        r = requests.get(request_url, headers=headers)
        return r.json()

    def getPrices(self, asin):
        method = 'GET'
        request_parameters = 'ItemCondition=new&MarketplaceId=ATVPDKIKX0DER'
        t = datetime.utcnow()
        amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        datestamp = t.strftime('%Y%m%d')
        canonical_uri = '/products/pricing/v0/items/' + asin + '/offers'
        canonical_querystring = request_parameters
        canonical_headers = 'host:' + self.host + '\n' + 'user-agent:' + self.amzUserAgent + '\n' + 'x-amz-access-token:' + self.tokenManager.accessToken + '\n' + 'x-amz-date:' + amzdate + '\n' + 'x-amz-security-token:' + self.tokenManager.spSecurityToken + '\n'
        signed_headers = 'host;user-agent;x-amz-access-token;x-amz-date;x-amz-security-token'
        payload_hash = hashlib.sha256(('').encode('utf-8')).hexdigest()
        canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = datestamp + '/' + self.region + '/' + self.service + '/' + 'aws4_request'
        string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
        signing_key = self.__getSignatureKey(self.tokenManager.spSecretAccessKey, datestamp, self.region, self.service)
        signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
        authorization_header = algorithm + ' ' + 'Credential=' + self.tokenManager.spAccessKeyId + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
        headers = {'user-agent' : self.amzUserAgent, 'x-amz-date':amzdate, 'x-amz-access-token': self.tokenManager.accessToken, 'x-amz-security-token': self.tokenManager.spSecurityToken, 'Authorization':authorization_header}
        request_url = self.endpoint + canonical_uri + '?' + canonical_querystring
        r = requests.get(request_url, headers=headers)
        noCompPrice = r.json()['payload']['Summary'].get('CompetitivePriceThreshold',True)
        return {
            "competitvePrice": r.json()['payload']['Summary']['CompetitivePriceThreshold']['Amount'] if noCompPrice == False else "No Compeitive Price",
            "lowestPrice": r.json()['payload']['Summary']['LowestPrices'][0]['LandedPrice']['Amount']
        }

    def getFees(self, asin, price):

        payload = '{'
        payload+= '"FeesEstimateRequest": {'
        payload+= '"MarketplaceId": "ATVPDKIKX0DER",'
        payload+=        '"IsAmazonFulfilled": True,'
        payload+=        '"PriceToEstimateFees": { "ListingPrice": {"CurrencyCode": "USD", "Amount":' + str(price) + '}},'
        payload+=        '"Identifier": "sample"'
        payload+=    '}'
        payload+= '}'

        print("payload String = " + payload)

        method = 'POST'
        request_parameters = ''
        t = datetime.utcnow()
        amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        datestamp = t.strftime('%Y%m%d')
        canonical_uri = '/products/fees/v0/items/' + asin + '/feesEstimate'
        canonical_querystring = request_parameters
        canonical_headers = 'host:' + self.host + '\n' + 'user-agent:' + self.amzUserAgent + '\n' + 'x-amz-access-token:' + self.tokenManager.accessToken + '\n' + 'x-amz-date:' + amzdate + '\n' + 'x-amz-security-token:' + self.tokenManager.spSecurityToken + '\n'
        signed_headers = 'host;user-agent;x-amz-access-token;x-amz-date;x-amz-security-token'
        payload_hash = hashlib.sha256((payload).encode('utf-8')).hexdigest()
        canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = datestamp + '/' + self.region + '/' + self.service + '/' + 'aws4_request'
        string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
        signing_key = self.__getSignatureKey(self.tokenManager.spSecretAccessKey, datestamp, self.region, self.service)
        signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
        authorization_header = algorithm + ' ' + 'Credential=' + self.tokenManager.spAccessKeyId + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
        headers = {'user-agent' : self.amzUserAgent, 'x-amz-date':amzdate, 'x-amz-access-token': self.tokenManager.accessToken, 'x-amz-security-token': self.tokenManager.spSecurityToken, 'Authorization':authorization_header}
        request_url = self.endpoint + canonical_uri
        r = requests.post(request_url, headers=headers, data=payload)
        return r.json()['payload']['FeesEstimateResult']['FeesEstimate']['TotalFeesEstimate']['Amount']

    # @checkExpiration
    def getPrepInstructions(self, asin):
        method = 'GET'
        request_parameters = 'ASINList=' + asin + '&ShipToCountryCode=US'
        t = datetime.utcnow()
        amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        datestamp = t.strftime('%Y%m%d')
        canonical_uri = '/fba/inbound/v0/prepInstructions'
        canonical_querystring = request_parameters
        canonical_headers = 'host:' + self.host + '\n' + 'user-agent:' + self.amzUserAgent + '\n' + 'x-amz-access-token:' + self.tokenManager.accessToken + '\n' + 'x-amz-date:' + amzdate + '\n' + 'x-amz-security-token:' + self.tokenManager.spSecurityToken + '\n'
        signed_headers = 'host;user-agent;x-amz-access-token;x-amz-date;x-amz-security-token'
        payload_hash = hashlib.sha256(('').encode('utf-8')).hexdigest()
        canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = datestamp + '/' + self.region + '/' + self.service + '/' + 'aws4_request'
        string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
        signing_key = self.__getSignatureKey(self.tokenManager.spSecretAccessKey, datestamp, self.region, self.service)
        signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
        authorization_header = algorithm + ' ' + 'Credential=' + self.tokenManager.spAccessKeyId + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
        headers = {'user-agent' : self.amzUserAgent, 'x-amz-date':amzdate, 'x-amz-access-token': self.tokenManager.accessToken, 'x-amz-security-token': self.tokenManager.spSecurityToken, 'Authorization':authorization_header}
        request_url = self.endpoint + canonical_uri + '?' + canonical_querystring
        r = requests.get(request_url, headers=headers)
        return r

