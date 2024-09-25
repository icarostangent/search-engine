from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HostViewSet, PortViewSet, SnapshotViewSet, ProxyViewSet

router = DefaultRouter()
router.register(r'snapshots', SnapshotViewSet)
router.register(r'hosts', HostViewSet)
router.register(r'ports', PortViewSet)
router.register(r'proxies', ProxyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
