import os
from django.core.management.base import BaseCommand
from internet.models import Word, WordList

class Command(BaseCommand):
    help = 'Import words from a file into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The file path to read words from')
        parser.add_argument('wordlist_name', type=str, help='Name of the word list to get or create')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        wordlist_name = kwargs['wordlist_name']

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File "{file_path}" does not exist'))
            return

        with open(file_path, 'r') as file:
            words = file.readlines()

        wordlist, _ = WordList.objects.get_or_create(name=wordlist_name)
        for line in words:
            line = line.strip()
            if line:
                word, _ = Word.objects.get_or_create(text=line)
                if wordlist not in word.lists.all():
                    word.lists.add(wordlist)

        self.stdout.write(self.style.SUCCESS('All words have been imported successfully'))
