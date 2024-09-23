import os
import subprocess
import json
import socket
from django.core.management.base import BaseCommand
from internet.models import Host, Port, Snapshot

class Command(BaseCommand):
    help = 'Run masscan and store results in the database'

    def add_arguments(self, parser):
        parser.add_argument('target', type=str, help='Target IP address or range')
        parser.add_argument('ports', type=str, default='1-65535', help='Ports to scan')

    def handle(self, *args, **kwargs):
        target = kwargs['target']
        ports = kwargs['ports']
        tmp_file = 'scan.json'
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
        ]
        proxies = {'tor': 9050}
        dead_proxies = []
        masscan_cmd = f'proxychains4 -f {proxychains_conf} masscan {target} --ports {ports} -oJ {tmp_file} --wait 0'
        
        for host, port in proxies.items():
            try:
                with socket.create_connection((host, port), timeout=1):
                    self.stdout.write(self.style.SUCCESS(f'Connected to {host}:{port} successfully'))
            except socket.timeout:
                self.stdout.write(self.style.ERROR(f'Timeout connecting to {host}:{port}'))
                dead_proxies.append(host)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error connecting to {host}:{port}: {e}'))
                dead_proxies.append(host)
        
        for host in dead_proxies:
            proxies.pop(host)
        
        if len(proxies) < 1:
            self.stdout.write(self.style.ERROR('No active proxies available. Exiting...'))
            return

        try:
            self.stdout.write(self.style.SUCCESS(f'Configuring proxychains')) 
            with open(proxychains_conf, 'w') as f:
                f.write('\n'.join(proxychains_data))

                for host, port in proxies.items():
                    f.write(f'\nsocks5\t{host}\t{port}\n')

        except:
            self.stdout.write(self.style.ERROR(f'Error writing proxychains config')) 

        self.stdout.write(self.style.SUCCESS(f'Running masscan command: {masscan_cmd}')) 
        subprocess.run(masscan_cmd, shell=True)

        with open(tmp_file, 'r') as file:
            try:
                data = json.load(file)
                # print(json.dumps(data, indent=4))
            except json.JSONDecodeError as e:
                print('Error decoding JSON:', e)
                exit(1)
        
        snapshot = Snapshot.objects.create()
        for datum in data:
            host, _ = Host.objects.get_or_create(host=datum['ip'], snapshot=snapshot)

            for port in datum['ports']:
                Port.objects.create(
                    port=port['port'], 
                    proto=port['proto'], 
                    status=port['status'], 
                    reason=port['reason'], 
                    ttl=port['ttl'],
                    host=host,
                    snapshot=snapshot,
                )

        self.stdout.write(self.style.SUCCESS(f'Cleaning up')) 
        os.remove(tmp_file)
        os.remove(proxychains_conf)

        self.stdout.write(self.style.SUCCESS(f'Scan completed')) 
