from django.contrib import messages
from django.shortcuts import render
from web.models import *
from django.http import JsonResponse

def context():
    all_category = Category.objects.all()
    all_brand = Brand.objects.all()
    all_product = Product.objects.all()
    all_voucher = Voucher.objects.all()
    return locals()

class BrandAdmin:
    def ad_brand(request):
        if 'submit_add_brand' in request.POST:
            list_name_category = request.POST.getlist("name_brand[]")
            for item in list_name_category:
                if item:
                    Brand(category_name=item).save()
            messages.success(request, "Thêm thương hiệu thành công!")
        if 'submit_update_brand' in request.POST:
            brand_id = request.POST["brand_update_id"]
            brand_name = request.POST["name_brand"]
            brand_obj = Brand.objects.get(pk=brand_id)
            brand_obj.brand_name = brand_name
            brand_obj.save()
            messages.success(request, "Cập nhật thương hiệu thành công!")
        return render(request, 'admin/brand.html', context())

    def ajax_get_brand(request):
        brand_id = request.POST["brand_id"]
        brand_detail = list(Brand.objects.filter(pk=brand_id).values())
        return JsonResponse(brand_detail, safe=False)