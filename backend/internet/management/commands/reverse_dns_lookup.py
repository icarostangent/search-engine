import subprocess
from django.core.management.base import BaseCommand
from django.db.models import Q
from internet.models import Host, Port, Domain

class Command(BaseCommand):
    help = 'Import words from a file into the database'

    def add_arguments(self, parser):
        parser.add_argument('ip', type=str, help='IP to check, otherwise check all entries')
        # parser.add_argument('proxychains', type=str, help='Use proxychains')

    def handle(self, *args, **kwargs):
        ip = kwargs['ip']

        if ip.lower() == 'all':
            targets = Port.objects.filter(Q(port_number=80) | Q(port_number=443))
        else:
            try:
                host = Host.objects.get(ip=ip)
            except:
                self.stdout.write(self.style.ERROR('Host does not exist in database.'))
                exit(1)

            try:
                targets = host.ports.filter(Q(port_number=80) | Q(port_number=443))
            except:
                self.stdout.write(self.style.ERROR('Port does not exist on host.'))
                exit(1)
        
        self.stdout.write(self.style.SUCCESS(f'Found {len(targets)} web targets.'))

        for target in targets:
            # lookup_cmd = ['/usr/bin/nslookup', '-timeout=2', str(target.host), '8.8.8.8']
            lookup_cmd = ['/usr/bin/dig', '-x', str(target.host), '@8.8.8.8', '+time=2']
            process = subprocess.Popen(lookup_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            output_by_line = []
            while True:
                output = process.stdout.readline()

                if output == '' and process.poll() is not None:
                    break

                output_by_line.append(output)

            begin_index = 0
            for index, line in enumerate(output_by_line):
                # print(line.strip())
                if 'ANSWER SECTION' in line:
                    begin_index = index
            
            if not begin_index:
                self.stdout.write(self.style.ERROR(f'No answer for host {str(target.host)}'))

            else:
                for line in output_by_line[begin_index:]:
                    if not ';;' in line:
                        if 'PTR' in line:
                            domain_name = line.split('PTR')[-1].strip()
                            Domain.objects.get_or_create(name=domain_name, host=target.host)
                            self.stdout.write(self.style.SUCCESS(f'Found {domain_name} for host {str(target.host)}'))
                        else:
                            pass
