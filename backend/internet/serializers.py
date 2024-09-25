from rest_framework import serializers
from .models import Host, Port, Snapshot, Proxy


class SnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snapshot
        fields = '__all__'


class PortSerializer(serializers.ModelSerializer):
    host = serializers.StringRelatedField()
    snapshot = serializers.StringRelatedField()

    class Meta:
        model = Port
        fields = '__all__'


class HostSerializer(serializers.ModelSerializer):
    ports = PortSerializer(many=True)
    snapshot = serializers.StringRelatedField()

    class Meta:
        model = Host
        fields = '__all__'


class ProxySerializer(serializers.ModelSerializer):
    class Meta:
        model = Proxy
        fields = '__all__'

