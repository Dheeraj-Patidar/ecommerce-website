# Generated by Django 4.1.3 on 2023-07-24 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_orderitem_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
