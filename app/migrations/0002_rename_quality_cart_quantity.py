# Generated by Django 4.0.4 on 2022-07-17 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='quality',
            new_name='quantity',
        ),
    ]
