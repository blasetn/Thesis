
import os
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse

from web.models import *
from web.adminfile.context import *


class ProductAdmin:
    def ad_product(request):
        if 'submit_add_product' in request.POST:
            try:
                pd_name = request.POST['product_name']
                pd_price = request.POST['product_price']
                if request.POST['product_pricesale'] == "":
                    pd_pricesale = None
                else:
                    pd_pricesale = request.POST['product_pricesale']
                pd_spec = request.POST['product_spec']
                pd_description = request.POST['product_description']
                pd_quantity = request.POST['product_quantity']
                pd_image = request.FILES['product_image']
                pd_images = request.FILES.getlist('product_images')
                category = Category.objects.get(pk=request.POST['product_category'])
                brand = Brand.objects.get(pk=request.POST['product_brand'])
                pd_status = request.POST['product_status']
                product_add = Product(pd_name=pd_name, pd_price=pd_price, pd_pricesale=pd_pricesale, pd_spec=pd_spec, pd_description=pd_description,
                                    pd_status=pd_status, pd_quantity=pd_quantity, category=category,brand =brand, pd_img=pd_image)
                product_add.save()
                product_id = Product.objects.get(pk=product_add.pk)
                for image in pd_images:
                    ImageProduct(ip_url=image, product=product_id).save()
                messages.success(request, "Thêm sản phẩm thành công!")
            except:
                messages.error(request, "Thêm không thành công!")
        if 'submit_update_product' in request.POST:
            try:
                product_id = request.POST['product_id']
                pd_name = request.POST['product_name']
                pd_price = request.POST['product_price']
                if request.POST['product_pricesale'] == "":
                    pd_pricesale = None
                else:
                    pd_pricesale = request.POST['product_pricesale']
                pd_spec = request.POST['product_spec']
                pd_description = request.POST['product_description']
                pd_quantity = request.POST['product_quantity']
                category = Category.objects.get(pk=request.POST['product_category'])
                brand = Brand.objects.get(pk=request.POST['product_brand'])
                pd_status = request.POST['product_status']
                if request.FILES.get('product_image',False):
                    try:
                        product = Product.objects.get(pk=product_id)
                        os.remove(product.pd_img.path)
                    except:
                        pass
                    pd_img = request.FILES['product_image']
                    a = Product.objects.get(pk=product_id)
                    a.pd_img = pd_img
                    a.save()
                Product.objects.filter(pk=product_id).update(pd_name=pd_name, pd_price=pd_price, pd_pricesale=pd_pricesale, pd_spec=pd_spec,
                                                            pd_description=pd_description, pd_status=pd_status,
                                                            pd_quantity=pd_quantity, category=category, brand=brand)
                if request.FILES.getlist('product_images', False):
                    product_id = Product.objects.get(pk=product_id)
                    image_old = ImageProduct.objects.filter(product=product_id)
                    for item in image_old:
                        os.remove(item.ip_url.path)
                    image_old.delete()
                    images = request.FILES.getlist('product_images')
                    for image in images:
                        ImageProduct(ip_url=image, product=product_id).save()
                messages.success(request, "Cập nhật sản phẩm thành công!")
            except:
                messages.error(request, "Cập nhật không thành công!")
        return render(request, 'admin/product.html', context())


    def ajax_get_product(request):
        try:
            product_id = request.POST["product_id"]
            product_detail = list(Product.objects.filter(pk=product_id).values())
            product_img = list(ImageProduct.objects.filter(
                product=product_id).values())
            context = {
                'product_detail': product_detail,
                'product_img': product_img
            }
            return JsonResponse(context)
        except:
            messages.error(request, "Lỗi không tìm thấy được mục yêu cầu!")
            return redirect('ad_product')