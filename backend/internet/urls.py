from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HostViewSet, PortViewSet, SnapshotViewSet, SocksProxyViewSet

router = DefaultRouter()
router.register(r'snapshots', SnapshotViewSet)
router.register(r'hosts', HostViewSet)
router.register(r'ports', PortViewSet)
router.register(r'proxies', SocksProxyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
