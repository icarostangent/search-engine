# Generated by Django 5.1.1 on 2024-09-26 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internet', '0009_remove_word_host_word_list'),
    ]

    operations = [
        migrations.RenameField(
            model_name='word',
            old_name='list',
            new_name='lists',
        ),
    ]
