# Generated by Django 3.2.13 on 2022-07-19 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management_system', '0004_item_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[('A', 'Active'), ('I', 'Inactive')], default='A', max_length=2),
        ),
    ]