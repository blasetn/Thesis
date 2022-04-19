from django.contrib import messages
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


def admin(request):
    return render(request, 'admin/index.html')


def category(request, id=None):
    all_category = Category.objects.all()
    if 'submit_category' in request.POST:
        list_name_category = request.POST.getlist("name_category[]")
        for item in list_name_category:
            if item:
                Category(category_name=item).save()
        messages.success(request, "Thêm danh mục thành công!")
    return render(request, 'admin/category.html', {'all_category': all_category, 'id': id})