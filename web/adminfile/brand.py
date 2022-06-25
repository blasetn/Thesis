from django.contrib import messages
from django.shortcuts import render, redirect
from web.models import *
from django.http import JsonResponse
from web.adminfile.context import *
from django.contrib.auth.decorators import login_required
from web.decorators import *

class BrandAdmin:
    @login_required(login_url='signin')
    @checkadmin
    def ad_brand(request):
        if 'submit_add_brand' in request.POST:
            try:
                list_name_brand = request.POST.getlist("name_brand[]")
                for item in list_name_brand:
                    if item:
                        Brand(brand_name=item).save()
                messages.success(request, "Thêm thương hiệu thành công!")
            except:
                messages.error(request, "Thêm không thành công!")
        if 'submit_update_brand' in request.POST:
            try:
                brand_id = request.POST["brand_update_id"]
                brand_name = request.POST["name_brand"]
                brand_status = request.POST["brand_status"]
                brand_obj = Brand.objects.get(pk=brand_id)
                brand_obj.brand_name = brand_name
                brand_obj.brand_status = brand_status
                brand_obj.save()
                messages.success(request, "Cập nhật thương hiệu thành công!")
            except:
                messages.error(request, "Cập nhật không thành công!")
        return render(request, 'admin/brand.html', context())

    @login_required(login_url='signin')
    @checkadmin
    def ajax_get_brand(request):
        try:
            brand_id = request.POST["brand_id"]
            brand_detail = list(Brand.objects.filter(pk=brand_id).values())
            return JsonResponse(brand_detail, safe=False)
        except:
            messages.error(request, "Lỗi không tìm thấy được mục yêu cầu!")
            return redirect('ad_category')