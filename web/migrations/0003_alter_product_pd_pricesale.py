# Generated by Django 4.0.3 on 2022-06-15 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_rename_category_date_created_brand_brand_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pd_pricesale',
            field=models.FloatField(null=True),
        ),
    ]
