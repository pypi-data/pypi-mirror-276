# Generated by Django 3.2.13 on 2022-06-01 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0031_pre_invoice_status_change'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.IntegerField(choices=[(0, 'Cart'), (10, 'Checkout'), (20, 'Complete')], default=0, verbose_name='Status'),
        ),
    ]
