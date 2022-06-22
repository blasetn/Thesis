# Generated by Django 4.0.3 on 2022-06-22 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('brand_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('brand_name', models.CharField(max_length=250, null=True)),
                ('brand_date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=250, null=True)),
                ('category_date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('order_time', models.DateTimeField(auto_now_add=True)),
                ('order_payment', models.CharField(default=0, max_length=5)),
                ('order_status', models.CharField(default=0, max_length=5, null=True)),
                ('order_code_payment', models.CharField(max_length=250, null=True)),
                ('order_ship', models.FloatField()),
                ('order_voucher_code', models.CharField(max_length=250, null=True)),
                ('order_discount', models.FloatField()),
                ('order_totalprice', models.FloatField()),
                ('order_name', models.CharField(max_length=250)),
                ('order_phone', models.CharField(max_length=11)),
                ('order_address', models.CharField(max_length=250)),
                ('order_email', models.EmailField(max_length=254, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('ud_fullname', models.CharField(max_length=250, null=True)),
                ('ud_sex', models.BooleanField(null=True)),
                ('ud_birthdate', models.DateField(null=True)),
                ('ud_phone', models.CharField(max_length=12, null=True)),
                ('ud_address', models.CharField(max_length=250, null=True)),
                ('ud_avatar', models.ImageField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('voucher_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('voucher_code', models.CharField(max_length=250)),
                ('voucher_value', models.FloatField()),
                ('voucher_quantity', models.PositiveSmallIntegerField(default=None, null=True)),
                ('voucher_date_created', models.DateTimeField(auto_now_add=True)),
                ('voucher_active', models.CharField(default=0, max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('pd_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('pd_name', models.CharField(max_length=250)),
                ('pd_price', models.FloatField()),
                ('pd_pricesale', models.FloatField(null=True)),
                ('pd_spec', models.TextField(null=True)),
                ('pd_description', models.TextField(null=True)),
                ('pd_status', models.CharField(default=0, max_length=5, null=True)),
                ('pd_view', models.PositiveBigIntegerField(default=0)),
                ('pd_date_created', models.DateTimeField(auto_now_add=True)),
                ('pd_quantity', models.PositiveSmallIntegerField(default=0)),
                ('pd_img', models.ImageField(upload_to='')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.category')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('od_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('od_nameproduct', models.CharField(max_length=250)),
                ('od_quantity', models.PositiveSmallIntegerField()),
                ('od_price', models.FloatField()),
                ('od_pricesale', models.FloatField(null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.product')),
            ],
        ),
        migrations.CreateModel(
            name='ImageProduct',
            fields=[
                ('ip_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ip_url', models.ImageField(upload_to='')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.product')),
            ],
        ),
    ]
