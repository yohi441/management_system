# Generated by Django 3.2.13 on 2022-07-12 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management_system', '0004_auto_20220712_1150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='date_pawned',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='redeem_date',
        ),
    ]
