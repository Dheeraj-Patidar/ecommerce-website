# Generated by Django 4.1.3 on 2023-07-31 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_alter_festivaldiscount_discount_percentage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='festivaldiscount',
            name='discount_percentage',
            field=models.IntegerField(default=10, null=True),
        ),
    ]
