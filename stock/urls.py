from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from stock.views import (
    StockViewSet,
    UserViewSet,
    TransactionViewSet
)

router = DefaultRouter()
router.register(r"stock", StockViewSet, basename="stock")
router.register(r"users", UserViewSet, basename="users")
router.register(r"transactions", TransactionViewSet, basename="transactions")

urlpatterns = [
    url(r"^", include(router.urls)),
]
