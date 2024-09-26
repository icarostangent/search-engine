from rest_framework import serializers
from .models import Host, Port, Proxy, Word, WordList



class PortSerializer(serializers.ModelSerializer):
    host = serializers.StringRelatedField()

    class Meta:
        model = Port
        fields = '__all__'


class ProxySerializer(serializers.ModelSerializer):
    class Meta:
        model = Proxy
        fields = '__all__'


class HostSerializer(serializers.ModelSerializer):
    ports = PortSerializer(many=True)
    proxy_endpoint = ProxySerializer(many=False)

    class Meta:
        model = Host
        fields = '__all__'


class Word_WordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordList
        fields = '__all__'


class WordSerializer(serializers.ModelSerializer):
    lists = Word_WordListSerializer(many=True)

    class Meta:
        model = Word
        fields = '__all__'


class WordListSerializer(serializers.ModelSerializer):
    words = WordSerializer(many=True)

    class Meta:
        model = WordList
        fields = '__all__'