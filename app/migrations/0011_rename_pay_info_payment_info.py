# Generated by Django 4.0.4 on 2022-11-02 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_delete_cart'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='pay_info',
            new_name='payment_info',
        ),
    ]
