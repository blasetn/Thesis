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


class CategoryAdmin:
    def category(request):
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
        return render(request, 'admin/category.html', context())

    def ajax_get_category(request):
        category_id = request.POST["category_id"]
        category_detail = list(Category.objects.filter(pk=category_id).values())
        return JsonResponse(category_detail, safe=False)