from unicodedata import category
from web.models import *
from django.shortcuts import render

class HomeUser:
    def home(request):
        count_cart = 0
        if 'cart' in request.session:
            cart = request.session['cart']
            for item in cart:
                count_cart += item.get('quantity')
        all_category = Category.objects.filter(category_status=0)
        all_brand = Brand.objects.filter(brand_status=0)
        mainbroad = Product.objects.filter(category=1, pd_status=1).order_by('-pd_id')[:3]
        vga = Product.objects.filter(category=4, pd_status=1).order_by('-pd_id')[:3]
        return render(request, 'home/index.html', locals())