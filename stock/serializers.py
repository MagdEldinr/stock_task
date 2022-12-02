from rest_framework import serializers
from .models import Stock, User

class StockSerializer(serializers.ModelSerializer):
    stock_id = serializers.CharField(required=False)
    price = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    availability = serializers.IntegerField(required=False)
    daily_highest_price = serializers.IntegerField(required=False)
    daily_lowest_price = serializers.IntegerField(required=False)
    hourly_highest_price = serializers.IntegerField(required=False)
    hourly_lowest_price = serializers.IntegerField(required=False)
    timestamp = serializers.DateTimeField(required=False, write_only=True)

    class Meta:
        model = Stock
        exclude = ('id', )

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
