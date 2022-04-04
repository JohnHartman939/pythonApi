class PricingAndSourceData():
    def __init__(self, price, useProvidedPrice=False):
        self.price = price
        self.source = 'using price from retailer api'
        if useProvidedPrice:
            self.source = 'using provided price'
        