# Generated by Django 5.1.1 on 2024-09-27 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internet', '0012_alter_wordlist_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='port',
            name='ttl',
            field=models.IntegerField(null=True),
        ),
    ]
