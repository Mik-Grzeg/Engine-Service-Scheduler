# Generated by Django 3.1.5 on 2021-02-25 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Clients', '0002_auto_20210225_2134'),
    ]

    operations = [
        migrations.RenameField(
            model_name='engine',
            old_name='_oph',
            new_name='oph',
        ),
    ]
