# Generated by Django 4.1.3 on 2023-08-29 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_alter_coupon_discount_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('black', 'BLACK'), ('blue', 'BLUE'), ('white', 'WHITE'), ('green', 'GREEN'), ('red', 'RED'), ('grey', 'GREY')], default=None, max_length=150, null=True)),
                ('colorcode', models.CharField(default=None, max_length=20, null=True)),
            ],
        ),
    ]
