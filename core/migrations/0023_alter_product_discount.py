# Generated by Django 4.1.3 on 2023-07-31 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_product_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.CharField(default=10, max_length=10),
        ),
    ]
