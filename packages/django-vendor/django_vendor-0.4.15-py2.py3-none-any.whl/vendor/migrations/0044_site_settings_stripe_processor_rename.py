# Generated by Django 3.2.19 on 2023-07-12 16:40

from django.db import migrations


def rename_stripe_processor_site_settings(apps, schema_editor):
    SiteConfigModel = apps.get_model('siteconfigs', 'SiteConfigModel')

    for site_setting in SiteConfigModel.objects.filter(key='vendor.config.PaymentProcessorSiteConfig', value__payment_processor='stripe_processor.StripeProcessor'):
        site_setting.value['payment_processor'] = 'stripe.StripeProcessor'
        site_setting.save()
        print(f"\nStripe Payment Processor Config Update for site {site_setting.site}")


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0043_invoice_global_discount'),
    ]

    operations = [
        migrations.RunPython(rename_stripe_processor_site_settings, reverse_code=migrations.RunPython.noop)
    ]
