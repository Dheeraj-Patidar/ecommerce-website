# Generated by Django 4.1.3 on 2023-07-29 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_product_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.ForeignKey(default='pending', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.productstatus'),
        ),
    ]
