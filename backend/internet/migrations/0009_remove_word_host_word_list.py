# Generated by Django 5.1.1 on 2024-09-26 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internet', '0008_wordlist_word_host'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='host',
        ),
        migrations.AddField(
            model_name='word',
            name='list',
            field=models.ManyToManyField(null=True, related_name='words', to='internet.wordlist'),
        ),
    ]
