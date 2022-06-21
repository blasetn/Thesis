from web.models import *

def context():
    all_category = Category.objects.all().order_by()
    all_brand = Brand.objects.all().order_by()
    all_product = Product.objects.all().order_by('-pd_id')
    all_voucher = Voucher.objects.all().order_by('-voucher_id')
    return locals()