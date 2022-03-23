from rest_framework import serializers

from recipes.nondbmodels.amazonModels import AmazonPriceSummary

class AmazonProductSerializer(serializers.Serializer):
    asin = serializers.CharField()
    title = serializers.CharField()
    imageUrl = serializers.CharField()
    salesRank = serializers.CharField()
    comptitivePrice = serializers.CharField()
    lowestPrice = serializers.CharField()
    feeTotal = serializers.CharField()
    restrictions = serializers.BooleanField()
    profit = serializers.CharField()
    profitability = serializers.CharField()
    profitPercentage = serializers.CharField()
    priceUsedSource = serializers.CharField()
    priceUsed = serializers.CharField()
    # lowestPrices = AmazonLowestPriceSerializer(many=True)
    # competitivePrice = AmazonCompetitivePriceSerializer()
    # lowestPrice = serializers.CharField(source='payload.Summary.LowestPrices[0].LandedPrice.Amount')
    # competitivePrice = serializers.CharField(source='payload.Summary.CompetitivePriceThreshold.Amount')

class AmazonPriceSummarySerializer(serializers.Serializer):

    low = serializers.CharField()
    comp = serializers.CharField()

    class Meta:
        model= AmazonPriceSummary
        fields= ['low', 'comp']
        # mapping_fields = (('high', 'low'), )
    def create(self, validated_data):
        return AmazonPriceSummary(validated_data.get('low'), validated_data.get('comp'))

# class AmazonLowestPriceSerializer(serializers.Serializer)
