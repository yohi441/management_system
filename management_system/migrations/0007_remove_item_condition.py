# Generated by Django 3.2.13 on 2022-07-12 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management_system', '0006_auto_20220712_1243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='condition',
        ),
    ]