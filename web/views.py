import os

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render

from web.models import *

# Home


def home(request):
    return render(request, 'home/index.html')


def signin(request):
    return render(request, 'home/signin.html')


def signup(request):
    return render(request, 'home/signup.html')


def account(request):
    return render(request, 'home/account.html')


def cart(request):
    return render(request, 'home/cart.html')


def checkout(request):
    return render(request, 'home/checkout.html')


def about(request):
    return render(request, 'home/about.html')


def blog(request):
    return render(request, 'home/blog.html')


def blogdetail(request):
    return render(request, 'home/blog-details.html')


def contact(request):
    return render(request, 'home/contact.html')


def shop(request):
    return render(request, 'home/shop.html')


def product(request):
    return render(request, 'home/product.html')


def search(request):
    return render(request, 'home/search.html')


# Admin

def context():
    all_category = Category.objects.all()
    all_product = Product.objects.all()
    all_voucher = Voucher.objects.all()
    return locals()

# @register.simple_tag
# def check_price_product(discount, active, start, end):
#     now = datetime.now()
#     result = True
#     if discount and active:
#         if not start and not end:
#             result = True
#         elif not start and end:
#             if now < end:
#                 result = True
#             else:
#                 result = False
#         elif not end and start:
#             if now > start:
#                 result = True
#             else:
#                 result = False
#         elif now > start and now < end:
#             result = True
#         else:
#             result = False
#     else:
#         result = False
#     return result


def admin(request):
    return render(request, 'admin/index.html')

# Admin Category


def category(request):
    if 'submit_add_category' in request.POST:
        list_name_category = request.POST.getlist("name_category[]")
        category_status = request.POST['category_status']
        for item in list_name_category:
            if item:
                Category(category_name=item,
                         category_status=category_status).save()
        messages.success(request, "Thêm danh mục thành công!")
    if 'submit_update_category' in request.POST:
        category_id = request.POST["category_update_id"]
        category_name = request.POST["name_category"]
        category_status = request.POST['category_status']
        category_obj = Category.objects.get(category_id)
        category_obj.category_name = category_name
        category_obj.category_status = category_status
        category_obj.save()
        messages.success(request, "Cập nhật danh mục thành công!")
    return render(request, 'admin/category.html', context())


def ajax_get_category(request):
    category_id = request.POST["category_id"]
    category_detail = list(Category.objects.filter(pk=category_id).values())
    return JsonResponse(category_detail, safe=False)

# Admin Product


def product(request):
    if 'submit_add_product' in request.POST:
        pd_name = request.POST['product_name']
        pd_price = request.POST['product_price']
        pd_spec = request.POST['product_spec']
        pd_description = request.POST['product_description']
        pd_quantity = request.POST['product_quantity']
        pd_img = request.FILES.getlist('product_images')
        category = Category.objects.get(pk=request.POST['product_category'])
        pd_status = request.POST['product_status']
        product_add = Product(pd_name=pd_name, pd_price=pd_price, pd_spec=pd_spec, pd_description=pd_description,
                              pd_status=pd_status, pd_quantity=pd_quantity, category=category)
        product_add.save()
        product_id = Product.objects.get(pk=product_add.pk)
        for image in pd_img:
            ImageProduct(ip_url=image, product=product_id).save()
        messages.success(request, "Thêm sản phẩm thành công!")
    if 'submit_update_product' in request.POST:
        product_id = request.POST['product_id']
        pd_name = request.POST['product_name']
        pd_price = request.POST['product_price']
        pd_spec = request.POST['product_spec']
        pd_description = request.POST['product_description']
        pd_quantity = request.POST['product_quantity']
        category = Category.objects.get(pk=request.POST['product_category'])
        pd_status = request.POST['product_status']
        Product.objects.filter(pk=product_id).update(pd_name=pd_name, pd_price=pd_price, pd_spec=pd_spec,
                                                     pd_description=pd_description, pd_status=pd_status,
                                                     pd_quantity=pd_quantity, category=category)
        if request.FILES.getlist('product_images', False):
            product_id = Product.objects.get(pk=product_id)
            image_old = ImageProduct.objects.filter(product=product_id)
            for item in image_old:
                os.remove(item.ip_url.path)
            image_old.delete()
            images = request.FILES.getlist('product_images')
            for image in images:
                ImageProduct(ip_url=image, product=product_id).save()
        messages.success(request, "Cập nhật sản phẩm thành công!")
    if 'submit_update_price_product' in request.POST:
        product_id = request.POST['product_price_id']
        pd_price = request.POST['product_price1']
        pdd_discount = request.POST['product_price2']
        pdd_avtive = request.POST['product_price_active']
        pdd_time = request.POST['product_price_time_active']
        product = Product.objects.get(pk=product_id)
        product.pd_price = pd_price
        product.save()
        try:
            product_discount = ProductDiscount.objects.get(pk=product)
            if product_discount:
                product_discount.pdd_discount = pdd_discount
                product_discount.pdd_active = pdd_avtive
                if pdd_time == '0':
                    product_discount.pdd_date_start = None
                    product_discount.pdd_date_end = None
                if pdd_time == '1':
                    if request.POST['product_price_datestart']:
                        product_discount.pdd_date_start = request.POST['product_price_datestart']
                    else:
                        product_discount.pdd_date_start = None
                    if request.POST['product_price_dateend']:
                        product_discount.pdd_date_end = request.POST['product_price_dateend']
                    else:
                        product_discount.pdd_date_end = None
                product_discount.save()
        except:
            ProductDiscount(
                product=product, pdd_discount=pdd_discount, pdd_active=pdd_avtive).save()
            if request.POST['product_price_datestart'] and request.POST['product_price_dateend']:
                ProductDiscount(pdd_date_start=request.POST['product_price_datestart'],
                                pdd_date_end=request.POST['product_price_dateend']).save()
        messages.success(request, "Cập nhật giá sản phẩm thành công!")
    return render(request, 'admin/product.html', context())


def ajax_get_product(request):
    product_id = request.POST["product_id"]
    product_detail = list(Product.objects.filter(pk=product_id).values())
    product_img = list(ImageProduct.objects.filter(
        product=product_id).values())
    product_price = list(Product.objects.filter(pk=product_id).values('pd_id', 'pd_price', 'productdiscount__pdd_discount',
                         'productdiscount__pdd_active', 'productdiscount__pdd_date_start', 'productdiscount__pdd_date_end'))
    context = {
        'product_detail': product_detail,
        'product_img': product_img,
        'product_price': product_price
    }
    return JsonResponse(context)


def voucher(request):
    if 'submit_add_voucher' in request.POST:
        voucher_code = request.POST['voucher_code']
        voucher_value_type = request.POST['voucher_value_type']
        voucher_value = float(request.POST['voucher_value'])
        voucher_quantity = request.POST['voucher_quantity']
        voucher_active = request.POST['voucher_active']
        voucher_time_active = request.POST['voucher_time_active']
        voucher_date_start = request.POST['voucher_date_start']
        voucher_date_end = request.POST['voucher_date_end']
        if voucher_value_type == "1":
            voucher_value /= 100.00
        if voucher_time_active == '0':
            voucher_date_start = None
            voucher_date_end = None
        if voucher_time_active == '1':
            if not voucher_date_start:
                voucher_date_start = None
            if not voucher_date_end:
                voucher_date_end = None
        if not voucher_quantity:
            voucher_quantity = None
        try:
            if Voucher.objects.get(voucher_code=voucher_code):
                messages.error(request, "Mã giảm giá đã tồn tại!")
        except:
            voucher_add = Voucher(voucher_code=voucher_code, voucher_value=voucher_value, voucher_date_start=voucher_date_start,
                            voucher_date_end=voucher_date_end, voucher_quantity=voucher_quantity, voucher_active=voucher_active)
            voucher_add.save()
            messages.success(request, "Thêm mã giảm giá thành công!")
    return render(request, 'admin/voucher.html', context())
