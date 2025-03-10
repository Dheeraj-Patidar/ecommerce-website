# Generated by Django 4.1.3 on 2023-07-18 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_product_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(default=None, max_length=10, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.size'),
        ),
    ]
