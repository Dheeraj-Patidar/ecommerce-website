# Generated by Django 4.1.3 on 2023-07-23 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_order_product_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='user',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.order'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='total',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
