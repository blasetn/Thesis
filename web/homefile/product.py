from django.shortcuts import render
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from web.models import *
from django.db.models import CharField, Lookup, TextField

class ProductUser:
    def shop(request, category=None, brand=None):
        count_cart = 0
        if 'cart' in request.session:
            cart = request.session['cart']
            for item in cart:
                count_cart += item.get('quantity')
        all_category = Category.objects.filter(category_status=0).order_by()
        all_brand = Brand.objects.filter(brand_status=0).order_by()
        all_product = Product.objects.filter(pd_status=1)
        if category:
            all_product = Product.objects.filter(category=category,pd_status=1)
        if brand:
            all_product = Product.objects.filter(brand=brand,pd_status=1)
        return render(request, 'home/shop.html', locals())

    def shopcategory(request, category=None):
        return ProductUser.shop(request, category=category, brand=None)

    def shopbrand(request, brand=None):
        return ProductUser.shop(request, category=None, brand=brand)


    def product(request, id=None):
        count_cart = 0
        if 'cart' in request.session:
            cart = request.session['cart']
            for item in cart:
                count_cart += item.get('quantity')
        all_category = Category.objects.filter(category_status=0).order_by()
        all_brand = Brand.objects.filter(brand_status=0).order_by()
        product = Product.objects.get(pk=id)
        product_images = ImageProduct.objects.filter(product=id)
        product_new = Product.objects.filter(pd_status=1).order_by('-pd_id')[:4]
        return render(request, 'home/product.html', locals())


    def search(request):
        count_cart = 0
        if 'cart' in request.session:
            cart = request.session['cart']
            for item in cart:
                count_cart += item.get('quantity')
        all_category = Category.objects.filter(category_status=0).order_by()
        all_brand = Brand.objects.filter(brand_status=0).order_by()
        result = None
        if request.method == 'GET':
            key_search = request.GET['key_search']
            vector = SearchVector('pd_name', 'brand__brand_name', 'category__category_name')
            query = SearchQuery(key_search)
            result = Product.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.001,pd_status=1).order_by('-rank')
            if not result:
                result = None
        else:
            result is None
        return render(request, 'home/search.html', locals())