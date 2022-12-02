from rest_framework.response import Response
from rest_framework import mixins, viewsets, permissions, status, exceptions
from rest_framework.decorators import action
from retry import retry

from .models import Stock, User
from .serializers import StockSerializer, UserSerializer
from .utilities import buy_stock, sell_stock

class StockViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    lookup_field = "stock_id"
    def retrieve(self, request, *args, **kwargs):
        try:
            self.queryset = self.get_queryset().get(**kwargs)
        except Stock.DoesNotExist:
            raise exceptions.NotFound("Stock not found")
        serializer = self.get_serializer(self.queryset, many=False)
        return Response(serializer.data)

class TransactionViewSet(viewsets.GenericViewSet,):
    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.AllowAny],
        url_path="buy",
        url_name="buy",
    )
    def buy(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.data.get("user_id"))
        except User.DoesNotExist:
            raise exceptions.NotFound("User id {} not found".format(request.data.get("user_id")))

        try:
            stock = Stock.objects.get(stock_id=request.data.get("stock_id"))
        except Stock.DoesNotExist:
            raise exceptions.NotFound("Stock id {} not found".format(request.data.get("stock_id")))

        if user.funds < stock.price * request.data.get("total"):
            return Response({"message":"No sufficient funds"},status=status.HTTP_403_FORBIDDEN)
        if stock.availability < request.data.get("total"):
            return Response({"message": "No enough stock"},status=status.HTTP_403_FORBIDDEN)
        
        try:
            buy_stock(user, stock, request.data.get("upper_bound"), request.data.get("lower_bound"), request.data.get("total"))
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response({"message":"Stock exceeded transaction bounds"},status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.AllowAny],
        url_path="sell",
        url_name="sell",
    )
    def sell(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.data.get("user_id"))
        except User.DoesNotExist:
            raise exceptions.NotFound("User id {} not found".format(request.data.get("user_id")))

        try:
            stock = Stock.objects.get(stock_id=request.data.get("stock_id"))
        except Stock.DoesNotExist:
            raise exceptions.NotFound("Stock id {} not found".format(request.data.get("stock_id")))
        try:
            sell_stock(user, stock, request.data.get("upper_bound"), request.data.get("lower_bound"), request.data.get("total"))
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response({"message":"Stock exceeded transaction bounds"},status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def retrieve(self, request, *args, **kwargs):
        self.queryset = self.get_queryset().get(**kwargs)
        serializer = self.get_serializer(self.queryset, many=False)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.AllowAny],
        url_path="deposit",
        url_name="deposit",
    )
    def deposit(self, request, *args, **kwargs):
        instance = User.objects.get(id=request.data.get("user_id"))
        instance.funds += request.data.get("amount")
        instance.save()
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.AllowAny],
        url_path="withdraw",
        url_name="withdraw",
    )
    def withdraw(self, request, *args, **kwargs):
        instance = User.objects.get(id=request.data.get("user_id"))
        instance.funds -= request.data.get("amount")
        instance.save()
        return Response(status=status.HTTP_200_OK)
