# Generated by Django 5.1.6 on 2025-02-17 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0002_alter_order_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='details', through='pos.OrderProduct', to='pos.product'),
        ),
    ]
