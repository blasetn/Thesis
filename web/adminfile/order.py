from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from web.models import Order, OrderDetail
from django.contrib.auth.decorators import login_required
from web.decorators import *


class OrderAdmin:
    @login_required(login_url='signin')
    @checkstaff
    def order(request):
        if 'submit_update_order' in request.POST:
            try:
                order_id = request.POST['order_id_update']
                order_status = request.POST['order_status']
                order_payment = request.POST['order_payment']
                order = Order.objects.get(pk=order_id)
                order.order_status = order_status
                order.order_payment = order_payment
                order.save()
                messages.success(request, "Cập nhật trạng thái đơn hàng thành công!")
            except:
                messages.error(request, "Cập nhật không thành công!")
        all_order = Order.objects.all().order_by('-order_id')
        return render(request, 'admin/order.html', locals())
    

    @login_required(login_url='signin')
    @checkstaff
    def ajax_get_order(request):
        try:
            order_id = request.POST["order_id"]
            order = list(Order.objects.filter(pk=order_id).values())
            order_detail = list(OrderDetail.objects.filter(order=order_id).values())
            context = {
                'order': order,
                'order_detail': order_detail
            }
            return JsonResponse(context)
        except:
            messages.error(request, "Lỗi không tìm thấy được mục yêu cầu!")
            return redirect('ad_order')