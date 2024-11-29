from django.urls import path
from rest_framework import routers
from .views import TransactionViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'transactions', TransactionViewSet, basename='transactions')

urlpatterns = router.urls
