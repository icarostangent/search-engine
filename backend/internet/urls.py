from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HostViewSet, DomainViewSet, PortViewSet, ProxyViewSet, 
    DNSRelayViewSet, WordViewSet, WordListViewSet
)

router = DefaultRouter()
router.register(r'hosts', HostViewSet)
router.register(r'domains', DomainViewSet)
router.register(r'ports', PortViewSet)
router.register(r'proxies', ProxyViewSet)
router.register(r'dnsrelays', DNSRelayViewSet)
router.register(r'words', WordViewSet)
router.register(r'wordlists', WordListViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
