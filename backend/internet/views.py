from rest_framework import viewsets
from .models import Host, Domain, Port, Proxy, DNSRelay, Word, WordList
from .serializers import (
    HostSerializer, DomainSerializer, PortSerializer, 
    ProxySerializer, DNSRelaySerializer, WordSerializer, WordListSerializer
)


class PortViewSet(viewsets.ModelViewSet):
    queryset = Port.objects.all()
    serializer_class = PortSerializer


class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer


class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer


class ProxyViewSet(viewsets.ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerializer


class DNSRelayViewSet(viewsets.ModelViewSet):
    queryset = DNSRelay.objects.all()
    serializer_class = DNSRelaySerializer


class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer


class WordListViewSet(viewsets.ModelViewSet):
    queryset = WordList.objects.all()
    serializer_class = WordListSerializer

