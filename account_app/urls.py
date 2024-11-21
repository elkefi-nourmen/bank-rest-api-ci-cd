from rest_framework import routers
from .views import AccountViewSet,BankViewSet,ClientViewSet

router=routers.DefaultRouter()
router.register(r'accounts',AccountViewSet,basename='accounts')
router.register(r'banks',BankViewSet,basename='banks')
router.register(r'clients',ClientViewSet,basename='clients')
urlpatterns = router.urls