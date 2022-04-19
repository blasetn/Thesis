# Generated by Django 4.0.3 on 2022-04-12 16:43

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
                ('order_code_payment', models.CharField(max_length=250)),
                ('order_ship', models.FloatField()),
                ('order_voucher_code', models.CharField(max_length=250, null=True)),
                ('order_discount', models.FloatField()),
                ('order_totalprice', models.FloatField()),
                ('order_name', models.CharField(max_length=250)),
                ('order_phone', models.CharField(max_length=11)),
                ('order_address', models.CharField(max_length=250)),
                ('order_email', models.EmailField(max_length=254, null=True)),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('pd_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('pd_name', models.CharField(max_length=250, null=True)),
                ('pd_price', models.FloatField()),
                ('pd_spec', models.TextField(null=True)),
                ('pd_description', models.TextField(null=True)),
                ('pd_status', models.CharField(default=0, max_length=5, null=True)),
                ('pd_view', models.PositiveBigIntegerField(default=0)),
                ('pd_date_created', models.DateTimeField(auto_now_add=True)),
                ('sp_quantity', models.PositiveSmallIntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.category')),
            ],
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
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
                ('voucher_exp', models.DateTimeField(null=True)),
                ('voucher_quantity', models.PositiveSmallIntegerField(null=True)),
                ('voucher_date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductDiscount',
            fields=[
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='web.product')),
                ('pdd_discount', models.FloatField()),
                ('pdd_active', models.BooleanField()),
                ('pdd_date_start', models.DateTimeField()),
                ('pdd_date_end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('first_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thread_first_person', to=settings.AUTH_USER_MODEL)),
                ('second_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thread_second_person', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('first_person', 'second_person')},
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('od_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('od_nameproduct', models.CharField(max_length=250)),
                ('od_quantity', models.PositiveSmallIntegerField()),
                ('od_price', models.FloatField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.product')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('news_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('news_title', models.CharField(max_length=250)),
                ('news_img', models.ImageField(upload_to='')),
                ('news_content', models.TextField()),
                ('news_status', models.IntegerField(default=0)),
                ('news_view', models.PositiveIntegerField(default=0)),
                ('news_date_created', models.DateTimeField(auto_now_add=True)),
                ('news_date_updated', models.DateTimeField(auto_now=True)),
                ('news_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
        migrations.CreateModel(
            name='ImageNews',
            fields=[
                ('img_news', models.BigAutoField(primary_key=True, serialize=False)),
                ('img_news_url', models.ImageField(upload_to='')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.news')),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('thread', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chatmessage_thread', to='web.thread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]