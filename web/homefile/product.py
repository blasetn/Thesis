from django.shortcuts import render 
from web.models import *

class ProductUser:
    def shop(request, id=None):
        all_category = Category.objects.all()
        all_product = Product.objects.all()
        if id:
            all_product = Product.objects.filter(category=id)
        return render(request, 'home/shop.html', locals())


    def product(request, id=None):
        all_category = Category.objects.all()
        product = Product.objects.get(pk=id)
        product_images = ImageProduct.objects.filter(product=id)
        product_new = Product.objects.all().order_by('-pd_id')[:4]
        return render(request, 'home/product.html', locals())


    def search(request):
        return render(request, 'home/search.html')