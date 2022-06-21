from django.shortcuts import render 
from web.models import *

class ProductUser:
    def shop(request, category=None, brand=None):
        all_category = Category.objects.all()
        all_brand = Brand.objects.all()
        all_product = Product.objects.all()
        if category:
            all_product = Product.objects.filter(category=category)
        if brand:
            all_product = Product.objects.filter(brand=brand)
        return render(request, 'home/shop.html', locals())

    def shopcategory(request, category=None):
        return ProductUser.shop(request, category=category, brand=None)

    def shopbrand(request, brand=None):
        return ProductUser.shop(request, category=None, brand=brand)


    def product(request, id=None):
        all_category = Category.objects.all()
        product = Product.objects.get(pk=id)
        product_images = ImageProduct.objects.filter(product=id)
        product_new = Product.objects.all().order_by('-pd_id')[:4]
        return render(request, 'home/product.html', locals())


    def search(request):
        return render(request, 'home/search.html')