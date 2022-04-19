from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class UserDetail(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    ud_fullname = models.CharField(max_length=250, null=True)
    ud_sex = models.BooleanField(null=True)
    ud_birthdate = models.DateField(null=True)
    ud_phone = models.CharField(max_length=12, null=True)
    ud_address = models.CharField(max_length=250, null=True)
    ud_avatar = models.ImageField(null=True)


class Category(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=250, null=True)
    category_date_created = models.DateTimeField(auto_now=False, auto_now_add=True)


class Product(models.Model):
    pd_id = models.BigAutoField(primary_key=True)
    pd_name = models.CharField(max_length=250, null=True)
    pd_price = models.FloatField()
    pd_spec = models.TextField(null=True)
    pd_description = models.TextField(null=True)
    pd_status = models.CharField(default=0, max_length=5, null=True)
    pd_view = models.PositiveBigIntegerField(default=0)
    pd_date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    sp_quantity = models.PositiveSmallIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class ProductDiscount(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    pdd_discount = models.FloatField()
    pdd_active = models.BooleanField()
    pdd_date_start = models.DateTimeField()
    pdd_date_end = models.DateTimeField()


class ImageProduct(models.Model):
    ip_id = models.BigAutoField(primary_key=True)
    ip_url = models.ImageField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Order(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    order_payment = models.CharField(max_length=5, default=0)
    order_status = models.CharField(max_length=5, null=True, default=0)
    order_code_payment = models.CharField(max_length=250)
    order_ship = models.FloatField()
    order_voucher_code = models.CharField(max_length=250, null=True)
    order_discount = models.FloatField()
    order_totalprice = models.FloatField()
    order_name = models.CharField(max_length=250)
    order_phone = models.CharField(max_length=11)
    order_address = models.CharField(max_length=250)
    order_email = models.EmailField(null=True)


class OrderDetail(models.Model):
    od_id = models.BigAutoField(primary_key=True)
    od_nameproduct = models.CharField(max_length=250)
    od_quantity = models.PositiveSmallIntegerField()
    od_price = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Voucher(models.Model):
    voucher_id = models.BigAutoField(primary_key=True)
    voucher_code = models.CharField(max_length=250)
    voucher_value = models.FloatField()
    voucher_exp = models.DateTimeField(null=True)
    voucher_quantity = models.PositiveSmallIntegerField(null=True)
    voucher_date_created = models.DateTimeField(auto_now=False, auto_now_add=True)


class News(models.Model):
    news_id = models.BigAutoField(primary_key=True)
    news_title = models.CharField(max_length=250)
    news_date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    news_img = models.ImageField()
    news_content = models.TextField()
    news_status = models.IntegerField(default=0)
    news_view = models.PositiveIntegerField(default=0)
    news_date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    news_date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    news_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class ImageNews(models.Model):
    img_news = models.BigAutoField(primary_key=True)
    img_news_url = models.ImageField()
    news = models.ForeignKey(News, on_delete=models.CASCADE)


class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()

    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE,
                               related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
