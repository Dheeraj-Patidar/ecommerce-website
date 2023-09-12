# Generated by Django 4.1.3 on 2023-07-27 07:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_orderitem_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='date',
            field=models.DateField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.CharField(default=None, max_length=20),
        ),
    ]
