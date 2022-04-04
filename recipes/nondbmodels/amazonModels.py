class ProfitabilityData:
    def __init__(self, asin, title, imageUrl, salesRank, prices, feeTotal, restrictions, retailPrice, priceUsedSource, labeling, prep):
        self.asin = asin
        self.title = title
        self.imageUrl = imageUrl
        self.salesRank = salesRank
        self.comptitivePrice = prices['competitvePrice']
        self.lowestPrice = prices['lowestPrice']
        self.feeTotal = feeTotal
        self.restrictions = restrictions
        self.profit = self.lowestPrice - self.feeTotal - retailPrice - retailPrice*.055
        self.profitPercentage = self.profit/retailPrice * 100
        self.priceUsedSource = priceUsedSource
        self.priceUsed = retailPrice
        self.profitability = self.getProfitabilityString(self.profitPercentage, self.profit, self.restrictions)
        self.labeling = labeling
        self.prep = prep

    def getProfitabilityString(self, profitPercentage, profit, restriction):
        if restriction:
            return "Do Not Buy, Restrictions"
        elif profit<3:
            return "Do Not Buy, Low Profit"
        elif profitPercentage<0:
            return "Do Not Buy"
        elif (profitPercentage>0) & (profitPercentage<= 35.0):
            return "Probably Do Not Buy"
        elif (profitPercentage>35) & (profitPercentage<= 65.0):
            return "Probably Buy"
        elif (profitPercentage>65) & (profitPercentage<= 100.0):
            return "Buy"
        elif (profitPercentage>100):
            return "Buy Now"
        else:
            return "Error"
class AmazonPriceSummary:
    def __init__(self, lowestPrice, competitivePrice) -> None:
        self.lowestPrice = lowestPrice
        self.competitivePrice = competitivePrice