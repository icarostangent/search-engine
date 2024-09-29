from rest_framework import serializers
from .models import Host, Domain, Port, Proxy, DNSRelay, Word, WordList



class PortSerializer(serializers.ModelSerializer):
    host = serializers.StringRelatedField()

    class Meta:
        model = Port
        fields = '__all__'


class ProxySerializer(serializers.ModelSerializer):
    class Meta:
        model = Proxy
        fields = '__all__'


class DomainSerializer(serializers.ModelSerializer):
    host = serializers.StringRelatedField()

    class Meta:
        model = Domain
        fields = '__all__'


class HostSerializer(serializers.ModelSerializer):
    ports = PortSerializer(many=True)
    domains = DomainSerializer(many=True)

    class Meta:
        model = Host
        fields = '__all__'


class DNSRelaySerializer(serializers.ModelSerializer):
    port = PortSerializer()
    class Meta:
        model = DNSRelay
        fields = '__all__'


class WordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordList
        fields = '__all__'


class WordSerializer(serializers.ModelSerializer):
    lists = WordListSerializer(many=True)

    class Meta:
        model = Word
        fields = '__all__'

