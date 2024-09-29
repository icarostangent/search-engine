import os
import subprocess
import json
import socket
from django.core.management.base import BaseCommand
from internet.models import Host, Port, Proxy
from internet.lib.proxychains import ProxyChainsConfigurator

class Command(BaseCommand):
    help = 'Run masscan and store results in the database'

    def add_arguments(self, parser):
        parser.add_argument('target', type=str, help='Target IP address or range')
        parser.add_argument('ports', type=str, default='1-65535', help='Ports to scan')
        parser.add_argument('use_proxychains', type=str, help='Use proxychains')

    def handle(self, *args, **kwargs):
        target = kwargs['target']
        ports = kwargs['ports']
        use_proxychains = kwargs['use_proxychains']

        if 'true' in use_proxychains.lower():
            proxychains = ProxyChainsConfigurator()
            masscan_cmd = ['proxychains4', '-f', proxychains.config_file, 'masscan', target, '--ports', ports, '--wait', '0', '--rate=100000', '--excludefile=masscan/exclude.conf']
            proxychains.set_strict_chain()

            self.stdout.write(self.style.SUCCESS(f'Configuring proxychains')) 

            for proxy in Proxy.objects.filter(enabled=True):
                proxychains.add_proxy(proxy.proxy_type, proxy.host_name, proxy.port_number)
                proxychains.write_config()

        else:
            masscan_cmd = ['masscan', target, '--ports', ports, '--wait', '0', '--rate=100000', '--excludefile=masscan/exclude.conf']

        self.stdout.write(self.style.SUCCESS(f'Running masscan command: {" ".join(masscan_cmd)}')) 

        process = subprocess.Popen(masscan_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        while True:
            output = process.stdout.readline()

            if output == '' and process.poll() is not None:
                break

            if 'Discovered open port' in output.strip():
                print(output.strip())

                output = output.split('Discovered open port')
                output = output[-1].split('on')
                host, _ = Host.objects.get_or_create(ip=output[-1].strip())

                output = output[0].split('/')
                port, _ = host.ports.get_or_create(port_number=output[0].strip(), proto=output[-1].strip())
