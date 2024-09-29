import subprocess
from django.core.management.base import BaseCommand
from internet.models import Host, Port, DNSRelay

class Command(BaseCommand):
    help = 'Import words from a file into the database'

    def add_arguments(self, parser):
        parser.add_argument('ip', type=str, help='IP to check, otherwise check all entries')
        # parser.add_argument('proxychains', type=str, help='Use proxychains')

    def handle(self, *args, **kwargs):
        ip = kwargs['ip']

        if ip.lower() == 'all':
            targets = Port.objects.filter(port_number=53)
        else:
            try:
                host = Host.objects.get(ip=ip)
            except:
                self.stdout.write(self.style.ERROR('Host does not exist in database.'))
                exit(1)

            try:
                targets = host.ports.filter(port_number=53)
            except:
                self.stdout.write(self.style.ERROR('Port does not exist on host.'))
                exit(1)
        
        self.stdout.write(self.style.SUCCESS(f'Found {len(targets)} DNS targets.'))

        for target in targets:
            nslookup_cmd = f'nslookup -timeout=2 google.com {target.host}'
            try:
                output = subprocess.run(nslookup_cmd, shell=True, capture_output=True, text=True)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error: {e}'))

            if 'google.com' in output.stdout:
                DNSRelay.objects.get_or_create(port=target)
                self.stdout.write(self.style.SUCCESS(f'Found open relay {target.host}'))