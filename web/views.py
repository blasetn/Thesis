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
        for item in list_name_category:
            if item:
                Category(category_name=item).save()
        messages.success(request, "Thêm danh mục thành công!")
    if 'submit_update_category' in request.POST:
        category_id = request.POST["category_update_id"]
        category_name = request.POST["name_category"]
        category_obj = Category.objects.get(pk=category_id)
        category_obj.category_name = category_name
        category_obj.save()
        messages.success(request, "Cập nhật danh mục thành công!")
    return render(request, 'admin/category.html', {'all_category': all_category})


def get_category(request):
    category_id = request.POST["category_id"]
    category_detail = list(Category.objects.values().filter(pk=category_id))
    return JsonResponse(category_detail, safe=False)
