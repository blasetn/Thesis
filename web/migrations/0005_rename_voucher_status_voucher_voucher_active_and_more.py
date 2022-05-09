# Generated by Django 4.0.3 on 2022-04-25 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_alter_productdiscount_pdd_date_end_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='voucher',
            old_name='voucher_status',
            new_name='voucher_active',
        ),
        migrations.RenameField(
            model_name='voucher',
            old_name='voucher_exp',
            new_name='voucher_date_end',
        ),
        migrations.AddField(
            model_name='voucher',
            name='voucher_date_start',
            field=models.DateTimeField(null=True),
        ),
    ]