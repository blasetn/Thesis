from django.contrib import messages
from django.shortcuts import redirect, render
from web.models import *
from django.http import JsonResponse
from web.adminfile.context import *
from django.contrib.auth.decorators import login_required
from web.decorators import *


class CategoryAdmin:
    @login_required(login_url='signin')
    @checkadmin
    def category(request):
        if 'submit_add_category' in request.POST:
            try:
                list_name_category = request.POST.getlist("name_category[]")
                for item in list_name_category:
                    if item:
                        Category(category_name=item).save()
                messages.success(request, "Thêm danh mục thành công!")
            except:
                messages.error(request, "Thêm không thành công!")
        if 'submit_update_category' in request.POST:
            try:
                category_id = request.POST["category_update_id"]
                category_name = request.POST["name_category"]
                category_status = request.POST["category_status"]
                category_obj = Category.objects.get(pk=category_id)
                category_obj.category_name = category_name
                category_obj.category_status = category_status
                category_obj.save()
                messages.success(request, "Cập nhật danh mục thành công!")
            except:
                messages.error(request, "Cập nhật không thành công!")
        return render(request, 'admin/category.html', context())

    @login_required(login_url='signin')
    @checkadmin
    def ajax_get_category(request):
        try:
            category_id = request.POST["category_id"]
            category_detail = list(Category.objects.filter(pk=category_id).values())
            return JsonResponse(category_detail, safe=False)
        except:
            messages.error(request, "Lỗi không tìm thấy được mục yêu cầu!")
            return redirect('ad_category')