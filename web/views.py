import os

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from web.models import *
from .decorators import *


def context():
    all_category = Category.objects.all()
    all_product = Product.objects.all()
    all_voucher = Voucher.objects.all()
    return locals()

# Home
def home(request):
    return render(request, 'home/index.html', context())


def signin(request):
    if 'signup' in request.POST:
        username = request.POST['signup_username']
        password = request.POST['signup_password']
        repassword = request.POST['signup_repassword']
        email = request.POST['signup_email']
        user_check = User.objects.filter(username=username)
        if user_check.count() < 1:
            if password == repassword:
                user = User.objects.create_user(username, email, password)
                user.save()
                user_id = User.objects.get(pk=user.id)
                UserDetail(user=user_id).save()
                messages.success(request, "Đăng ký thành công!")
            else:
                messages.error(request, "Đăng ký không thành công: Mật khẩu và nhập lại mật khẩu không khớp!")
        else:
            messages.error(request, "Đăng ký không thành công: Tài khoản đã tồn tại!")
    if 'signin' in request.POST:
        username = request.POST['signin_username']
        password = request.POST['signin_password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            messages.error(request, "Đăng nhập không thành công: Sai tài khoản hoặc mật khẩu!")
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'home/signin.html', context())


def account(request):
    all_category = Category.objects.all()
    if request.user.is_authenticated:
        user_detail = UserDetail.objects.get(pk=request.user.id)
        if 'update' in request.POST:
            user_detail.ud_fullname = request.POST['fullname']
            user_detail.ud_sex = request.POST['sex']
            user_detail.ud_birthdate = request.POST['birthdate']
            user_detail.ud_phone = request.POST['phone']
            user_detail.ud_address = request.POST['address']
            if request.FILES.get('user_avatar', False):
                try:
                    os.remove(user_detail.ud_avatar.path)
                except:
                    pass
                user_detail.ud_avatar = request.FILES['user_avatar']
            user_detail.save()
            user = User.objects.get(pk=request.user.id)
            user.email = request.POST['email']
            user.save()
            messages.success(request, "Cập nhật tài khoản thành công!")
            return redirect('account')
        if 'changepass' in request.POST:
            password_old = request.POST['password_old']
            password_new = request.POST['password_new']
            re_password_new = request.POST['re_password_new']
            user = authenticate(request, username=request.user.username, password=password_old)
            if user is not None:
                if password_new == re_password_new:
                    user.set_password(password_new)
                    user.save()
                    messages.success(request, "Đổi mật khẩu thành công!")
                else:
                    messages.error(request, "Đổi mật khẩu không thành công: Mật khẩu và nhập lại mật khẩu mới không khớp!")
            else:
                messages.error(request, "Đổi mật khẩu không thành công: Mật khẩu cũ không đúng!")
            return redirect('account')
        return render(request, 'home/account.html', locals())
    else:
        return redirect('signin')


def user_logout(request):
    logout(request)
    return redirect('home')


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


def shop(request, id=None):
    all_category = Category.objects.all()
    all_product = Product.objects.all().values('pd_id', 'pd_name', 'pd_price', 'imageproduct__ip_url')
    if id==1:
        all_category = Category.objects.all()[:2]
    return render(request, 'home/shop.html', locals())


def product(request):
    return render(request, 'home/product.html', locals())


def search(request):
    return render(request, 'home/search.html')


# Admin
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


def ad_product(request):
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
    if 'submit_update_voucher' in request.POST:
        voucher_id = request.POST['voucher_id']
        voucher_code = request.POST['voucher_code']
        voucher_value_type = request.POST['voucher_value_type']
        voucher_value = float(request.POST['voucher_value'])
        voucher_quantity = request.POST['voucher_quantity']
        voucher_active = request.POST['voucher_active']
        voucher_time_active = request.POST['voucher_time_active']
        voucher_date_start = request.POST['voucher_date_start']
        voucher_date_end = request.POST['voucher_date_end']
        voucher_update = Voucher.objects.get(pk=voucher_id)
        voucher_update.code = voucher_code
        if voucher_value_type == "1":
            voucher_value /= 100.00
        voucher_update.voucher_value = voucher_value
        if voucher_time_active == '1':
            if not voucher_date_start:
                voucher_date_start = None
            if not voucher_date_end:
                voucher_date_end = None
        voucher_update.voucher_date_start = voucher_date_start
        voucher_update.voucher_date_end = voucher_date_end
        if not voucher_quantity:
            voucher_quantity = None
        voucher_update.voucher_quantity = voucher_quantity
        voucher_update.voucher_active = voucher_active
        voucher_update.save()
        messages.success(request, "Cập nhật mã giảm giá thành công!")
    return render(request, 'admin/voucher.html', context())


def ajax_get_voucher(request):
    voucher_id = request.POST["voucher_id"]
    voucher_detail = list(Voucher.objects.filter(pk=voucher_id).values())
    context = {
        'voucher_detail': voucher_detail
    }
    return JsonResponse(context)