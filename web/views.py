import os
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from regex import F
from tomlkit import array

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


def admin(request):
    return render(request, 'admin/index.html')


def category(request):
    all_category = Category.objects.all()
    if 'submit_add_category' in request.POST:
        list_name_category = request.POST.getlist("name_category[]")
        category_status = request.POST['category_status']
        for item in list_name_category:
            if item:
                Category(category_name=item, category_status=category_status).save()
        messages.success(request, "Thêm danh mục thành công!")
    if 'submit_update_category' in request.POST:
        category_id = request.POST["category_update_id"]
        category_name = request.POST["name_category"]
        category_status = request.POST['category_status']
        category_obj = Category.objects.get(pk=category_id)
        category_obj.category_name = category_name
        category_obj.category_status = category_status
        category_obj.save()
        messages.success(request, "Cập nhật danh mục thành công!")
    return render(request, 'admin/category.html', {'all_category': all_category})


def get_category(request):
    category_id = request.POST["category_id"]
    category_detail = list(Category.objects.filter(pk=category_id).values())
    return JsonResponse(category_detail, safe=False)


def product(request):
    all_product = Product.objects.all()
    all_category = Category.objects.all()
    if 'submit_add_product' in request.POST:
        pd_name = request.POST['product_name']
        pd_price = request.POST['product_price']
        pd_spec = request.POST['product_spec']
        pd_description = request.POST['product_description']
        pd_quantity = request.POST['product_quantity']
        pd_img = request.FILES.getlist('product_images')
        category = Category.objects.get(pk=request.POST['product_category'])
        pd_status = request.POST['product_status']
        product_add = Product(pd_name=pd_name, pd_price=pd_price, pd_spec=pd_spec, pd_description=pd_description, pd_status=pd_status, pd_quantity=pd_quantity,
                              category=category)
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
            # test = ImageProduct.objects.get(pk=4)
            for item in image_old:
                os.remove(item.ip_url.path)
            image_old.delete()
            images = request.FILES.getlist('product_images')
            for image in images:
                ImageProduct(ip_url=image, product=product_id).save()
        messages.success(request, "Cập nhật sản phẩm thành công!")
    return render(request, 'admin/product.html', {'products': all_product, 'categorys': all_category})


def get_product(request):
    product_id = request.POST["product_id"]
    product_detail = list(Product.objects.values().filter(pk=product_id))
    product_img = list(ImageProduct.objects.values().filter(product=product_id))
    product_price = list(Product.objects.values('pd_id', 'pd_price', 'productdiscount__pdd_discount', 'productdiscount__pdd_active', 'productdiscount__pdd_date_start', 'productdiscount__pdd_date_end'))
    return JsonResponse({'product_detail': product_detail, 'product_img': product_img, 'product_price': product_price})


