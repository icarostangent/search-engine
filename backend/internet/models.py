import uuid
from django.db import models


class Snapshot(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.uuid)


class Host(models.Model):
    host = models.GenericIPAddressField(unique=True)
    snapshot = models.ForeignKey(Snapshot, related_name='hosts', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.host)


class Port(models.Model):
    port = models.IntegerField()
    proto = models.CharField(max_length=3)
    status = models.CharField(max_length=25)
    reason = models.CharField(max_length=25)
    ttl = models.IntegerField()
    host = models.ForeignKey(Host, related_name='ports', on_delete=models.CASCADE)
    snapshot = models.ForeignKey(Snapshot, related_name='ports', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.port)


class Proxy(models.Model):
    proxy_types = {'S4': 'socks4', 'S5': 'socks5', 'HP': 'HTTP', 'HS': 'HTTPS',}

    host = models.CharField(max_length=255)
    port = models.IntegerField()
    type = models.CharField(max_length=2, choices=proxy_types)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.host}:{self.port}"
