from rest_framework import viewsets
from .models import Host, Port, Proxy, Word, WordList
from .serializers import HostSerializer, PortSerializer, ProxySerializer, WordSerializer, WordListSerializer


class PortViewSet(viewsets.ModelViewSet):
    queryset = Port.objects.all()
    serializer_class = PortSerializer


class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer


class ProxyViewSet(viewsets.ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerializer


class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer


class WordListViewSet(viewsets.ModelViewSet):
    queryset = WordList.objects.all()
    serializer_class = WordListSerializer

