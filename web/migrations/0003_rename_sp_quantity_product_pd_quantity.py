# Generated by Django 4.0.3 on 2022-04-22 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_category_category_status_voucher_voucher_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='sp_quantity',
            new_name='pd_quantity',
        ),
    ]