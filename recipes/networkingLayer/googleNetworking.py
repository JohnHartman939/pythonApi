import requests

def getPlaces(location):
    params = Params(location=location, rankby ='distance', type = 'department_store', key = 'AIzaSyCbyfAxzRscrKMXVDIaNOkH1GDAP89eCIQ')
    stores = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json', params=params.data)
    return stores

def getAddressForPlace(placeId):
    # params = Params(place_id=placeId, key = 'AIzaSyCbyfAxzRscrKMXVDIaNOkH1GDAP89eCIQ')
    params = Params(fields="formatted_address", place_id=placeId, key = 'AIzaSyCbyfAxzRscrKMXVDIaNOkH1GDAP89eCIQ')
    placeAddress = requests.get('https://maps.googleapis.com/maps/api/place/details/json', params=params.data)
    return placeAddress

class Params:
    def __init__(self, **kwargs) -> None:
        self.data = {}
        for key, value in kwargs.items():
            self.data.update({key: value})
