import os
from django.core.management.base import BaseCommand
from internet.models import Word 

class Command(BaseCommand):
    help = 'Import words from a file into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The file path to read words from')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File "{file_path}" does not exist'))
            return

        with open(file_path, 'r') as file:
            words = file.readlines()

        for word in words:
            word = word.strip()
            if word:
                Word.objects.get_or_create(text=word)

        self.stdout.write(self.style.SUCCESS('All words have been imported successfully'))
