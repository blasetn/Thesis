from web.models import *
from django.shortcuts import render

class HomeUser:
    def home(request):
        all_category = Category.objects.all()
        all_brand = Brand.objects.all()
        product_new = Product.objects.all().order_by('-pd_id')[:3]
        return render(request, 'home/index.html', locals())