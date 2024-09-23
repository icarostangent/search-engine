from rest_framework import viewsets
from .models import Host, Port, Snapshot, SocksProxy
from .serializers import HostSerializer, PortSerializer, SnapshotSerializer, SocksProxySerializer


class SnapshotViewSet(viewsets.ModelViewSet):
    queryset = Snapshot.objects.all()
    serializer_class = SnapshotSerializer


class PortViewSet(viewsets.ModelViewSet):
    queryset = Port.objects.all()
    serializer_class = PortSerializer


class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer


class SocksProxyViewSet(viewsets.ModelViewSet):
    queryset = SocksProxy.objects.all()
    serializer_class = SocksProxySerializer
