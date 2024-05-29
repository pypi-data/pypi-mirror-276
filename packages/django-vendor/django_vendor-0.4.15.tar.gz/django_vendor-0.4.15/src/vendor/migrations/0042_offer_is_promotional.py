# Generated by Django 3.2.19 on 2023-05-08 16:39

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0041_offer_billing_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='is_promotional',
            field=models.BooleanField(default=False, help_text='You can mark this offer as promotional to help identify it between normal priced and discount priced offers.', verbose_name='Is Promotional'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=True, populate_from='name', unique_with=('site__id',)),
        ),
    ]
