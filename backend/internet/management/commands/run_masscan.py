import os
import subprocess
import json
import socket
from django.core.management.base import BaseCommand
from internet.models import Host, Port, Proxy

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
        masscan_output_file = 'scan.json'
        proxychains_conf = 'proxychains.conf'
        proxychains_data = [
            # 'random_chain',
            # 'dynamic_chain',
            'strict_chain',
            'proxy_dns',
            'remote_dns_subnet 224',
            'tcp_read_time_out 15000',
            'tcp_connect_time_out 8000',
            'localnet 127.0.0.0/255.0.0.0',
            '',
            '[ProxyList]',
            '',
        ]
        proxy_types = {'S4': 'socks4', 'S5': 'socks5', 'HP': 'http', 'HS': 'https'}
        # proxies = {'tor': 9050}

        if use_proxychains.lower() =='true':
            masscan_cmd = f'proxychains4 -f {proxychains_conf} masscan {target} --ports {ports} -oJ {masscan_output_file} --wait 0 --rate=100000 --excludefile=masscan/exclude.conf'
            proxies = Proxy.objects.filter(enabled=True)
            dead_proxies = []

            self.stdout.write(self.style.SUCCESS(f'Using proxychains'))
        
            for proxy in proxies:
                try:
                    with socket.create_connection((proxy.host_name, proxy.port_number), timeout=1):
                        self.stdout.write(self.style.SUCCESS(f'Connected to {proxy.host_name}:{proxy.port_number} successfully'))
                except socket.timeout:
                    self.stdout.write(self.style.ERROR(f'Timeout connecting to {proxy.host_name}:{proxy.port_number}'))
                    proxy.dead = True
                    proxy.save()
                    dead_proxies.append(proxy)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error connecting to {proxy.host_name}:{proxy.port_number}: {e}'))
                    proxy.dead = True
                    proxy.save()
                    dead_proxies.append(proxy)
            
            for proxy in dead_proxies:
                proxies.pop(proxy)
            
            if len(proxies) < 1:
                self.stdout.write(self.style.ERROR('No active proxies available. Exiting...'))
                return

            try:
                self.stdout.write(self.style.SUCCESS(f'Configuring proxychains')) 
                with open(proxychains_conf, 'w') as f:
                    f.write('\n'.join(proxychains_data))

                    for proxy in proxies:
                        f.write(f'{proxy_types[proxy.proxy_type]}\t{proxy.host_name}\t{proxy.port_number}\n')

            except:
                self.stdout.write(self.style.ERROR(f'Error writing proxychains config')) 
                exit(1)

        else: # use_proxychains = false
            masscan_cmd = f'masscan {target} --ports {ports} -oJ {masscan_output_file} --wait 0 --rate=100000 --excludefile=masscan/exclude.conf'

        self.stdout.write(self.style.SUCCESS(f'Running masscan command: {masscan_cmd}')) 
        try:
            subprocess.run(masscan_cmd, shell=True, capture_output=True, text=True, check=True)
        except:
            self.stdout.write(self.style.ERROR('Masscan failed please try again.'))
            exit(1)

        with open(masscan_output_file, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                print('Error decoding JSON. Cleaning up.')
                os.remove(masscan_output_file)
                if use_proxychains.lower() == 'true':
                    os.remove(proxychains_conf)
                exit(1)
        
        for datum in data:
            host, _ = Host.objects.get_or_create(ip=datum['ip'])
            if use_proxychains.lower() == 'true':
                host.proxy_endpoint = proxies.last()
                host.save()

            for new_port in datum['ports']:
                for port in host.ports.all():
                    if port.port_number == new_port['port']:
                        port.delete()

                self.stdout.write(self.style.SUCCESS(f'Found port: {new_port}')) 
                Port.objects.create(
                    port_number=new_port['port'], 
                    proto=new_port['proto'], 
                    status=new_port['status'], 
                    reason=new_port['reason'], 
                    ttl=new_port['ttl'],
                    host=host,
                )

        self.stdout.write(self.style.SUCCESS(f'Cleaning up')) 
        os.remove(masscan_output_file)
        if use_proxychains.lower() == 'true':
            os.remove(proxychains_conf)

        self.stdout.write(self.style.SUCCESS(f'Scan completed')) 
