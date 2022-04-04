def makeParams( **kwargs):
        data = {}
        for key, value in kwargs.items():
            data.update({key:value})
        return data