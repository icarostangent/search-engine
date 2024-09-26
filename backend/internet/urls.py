from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HostViewSet, PortViewSet, ProxyViewSet, WordViewSet, WordListViewSet

router = DefaultRouter()
router.register(r'hosts', HostViewSet)
router.register(r'ports', PortViewSet)
router.register(r'proxies', ProxyViewSet)
router.register(r'words', WordViewSet)
router.register(r'wordlists', WordListViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
