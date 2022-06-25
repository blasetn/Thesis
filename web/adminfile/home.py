from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from web.decorators import *
from web.models import *

class HomeAdmin:
    @login_required(login_url='signin')
    @checkstaff
    def admin(request):
        count_product = Product.objects.count()
        product_new = Product.objects.all().order_by('-pd_id')[:5]
        count_order = Order.objects.count()
        order_new = Order.objects.all().order_by('-order_id')[:5]
        count_customer = User.objects.filter(is_staff=False, is_superuser=False).count()
        customer_new = User.objects.filter(is_staff=False, is_superuser=False).order_by('-id')[:5]
        count_voucher = Voucher.objects.filter(voucher_active=1).count()
        return render(request, 'admin/index.html', locals())