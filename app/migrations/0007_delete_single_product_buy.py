# Generated by Django 4.0.4 on 2022-07-22 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_single_product_buy_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='single_product_buy',
        ),
    ]