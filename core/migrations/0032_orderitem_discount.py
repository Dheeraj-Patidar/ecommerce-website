# Generated by Django 4.1.3 on 2023-08-07 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_alter_coupon_coupon_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='discount',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
