import uuid
from django.db import models


class Host(models.Model):
    ip = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return str(self.ip)


class Port(models.Model):
    port_number = models.IntegerField()
    proto = models.CharField(max_length=3)
    status = models.CharField(max_length=25)
    reason = models.CharField(max_length=25)
    ttl = models.IntegerField(null=True)
    host = models.ForeignKey('Host', related_name='ports', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.port_number)


class Proxy(models.Model):
    proxy_types = {'S4': 'socks4', 'S5': 'socks5', 'HP': 'HTTP', 'HS': 'HTTPS',}

    host_name = models.CharField(max_length=255)
    port_number = models.IntegerField()
    proxy_type = models.CharField(max_length=2, choices=proxy_types)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    enabled = models.BooleanField(default=True)
    dead = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.proxy_type}:{self.host_name}:{self.port_number}"


class HostName(models.Model):
    name = models.Field(max_length=255)
    host = models.ForeignKey('Host', related_name='host_names', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class DNSRelay(models.Model):
    port = models.OneToOneField('Port', related_name='dns_relay', on_delete=models.CASCADE)

    def __str__(self):
        return str(True)


class Word(models.Model):
    text = models.CharField(max_length=255, unique=True)
    lists = models.ManyToManyField('WordList', related_name='words')

    def __str__(self):
        return str(self.text)


class WordList(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)