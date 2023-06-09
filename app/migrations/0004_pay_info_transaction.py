# Generated by Django 4.0.4 on 2022-07-19 20:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_alter_customer_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='pay_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_data', models.TextField(max_length=100000000000000000000000000000000000, null=True)),
                ('ORDERID', models.CharField(max_length=900000000, null=True)),
                ('MID', models.CharField(max_length=900000000, null=True)),
                ('TXNID', models.CharField(max_length=900000000, null=True)),
                ('TXNAMOUNT', models.CharField(max_length=900000000, null=True)),
                ('PAYMENTMODE', models.CharField(max_length=900000000, null=True)),
                ('CURRENCY', models.CharField(max_length=900000000, null=True)),
                ('TXNDATE', models.CharField(max_length=900000000, null=True)),
                ('STATUS', models.CharField(max_length=900000000, null=True)),
                ('RESPCODE', models.CharField(max_length=900000000, null=True)),
                ('RESPMSG', models.CharField(max_length=900000000, null=True)),
                ('GATEWAYNAME', models.CharField(max_length=900000000, null=True)),
                ('BANKTXNID', models.CharField(max_length=900000000, null=True)),
                ('BANKNAME', models.CharField(max_length=900000000, null=True)),
                ('CHECKSUMHASH', models.CharField(max_length=900000000, null=True)),
                ('message', models.CharField(max_length=900000000, null=True)),
                ('current_date_time', models.CharField(max_length=100000000000000000000, null=True)),
                ('expiry_date_time', models.CharField(max_length=100000000000000000000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('made_on', models.DateTimeField(auto_now_add=True)),
                ('amount', models.CharField(max_length=10000000000000000000000000000000000000000000000000000)),
                ('order_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('checksum', models.CharField(blank=True, max_length=100, null=True)),
                ('made_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
