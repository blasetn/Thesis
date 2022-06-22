import os
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse

from web.models import *
from web.adminfile.context import *
from django.contrib.auth.decorators import login_required
from web.decorators import *


class VoucherAdmin:
    @login_required(login_url='signin')
    @checkadmin
    def voucher(request):
        if 'submit_add_voucher' in request.POST:
            try:
                voucher_code = request.POST['voucher_code']
                voucher_value_type = request.POST['voucher_value_type']
                voucher_value = float(request.POST['voucher_value'])
                voucher_quantity = request.POST['voucher_quantity']
                voucher_active = request.POST['voucher_active']
                # voucher_time_active = request.POST['voucher_time_active']
                # voucher_date_start = request.POST['voucher_date_start']
                # voucher_date_end = request.POST['voucher_date_end']
                if voucher_value_type == "1":
                    voucher_value /= 100.00
                # if voucher_time_active == '0':
                #     voucher_date_start = None
                #     voucher_date_end = None
                # if voucher_time_active == '1':
                #     if not voucher_date_start:
                #         voucher_date_start = None
                #     if not voucher_date_end:
                #         voucher_date_end = None
                if not voucher_quantity:
                    voucher_quantity = None
                try:
                    if Voucher.objects.get(voucher_code=voucher_code):
                        messages.error(request, "Mã giảm giá đã tồn tại!")
                except:
                    voucher_add = Voucher(voucher_code=voucher_code, voucher_value=voucher_value,voucher_quantity=voucher_quantity, voucher_active=voucher_active)
                    voucher_add.save()
                    messages.success(request, "Thêm mã giảm giá thành công!")
            except:
                messages.error(request, "Thêm mã giảm giá không thành công!")
        if 'submit_update_voucher' in request.POST:
            try:
                voucher_id = request.POST['voucher_id']
                voucher_code = request.POST['voucher_code']
                voucher_value_type = request.POST['voucher_value_type']
                voucher_value = float(request.POST['voucher_value'])
                voucher_quantity = request.POST['voucher_quantity']
                voucher_active = request.POST['voucher_active']
                # voucher_time_active = request.POST['voucher_time_active_update']
                # voucher_date_start = request.POST['voucher_date_start']
                # voucher_date_end = request.POST['voucher_date_end']
                voucher_update = Voucher.objects.get(pk=voucher_id)
                voucher_update.code = voucher_code
                if voucher_value_type == "1":
                    voucher_value /= 100.00
                voucher_update.voucher_value = voucher_value
                # if voucher_time_active == '0':
                #     voucher_date_start = None
                #     voucher_date_end = None
                # if voucher_time_active == '1':
                #     if not voucher_date_start:
                #         voucher_date_start = None
                #     if not voucher_date_end:
                #         voucher_date_end = None
                # voucher_update.voucher_date_start = voucher_date_start
                # voucher_update.voucher_date_end = voucher_date_end
                if not voucher_quantity:
                    voucher_quantity = None
                voucher_update.voucher_quantity = voucher_quantity
                voucher_update.voucher_active = voucher_active
                voucher_update.save()
                messages.success(request, "Cập nhật mã giảm giá thành công!")
            except:
                messages.error(request, "Cập nhật mã giảm giá không thành công!")
        return render(request, 'admin/voucher.html', context())


    @login_required(login_url='signin')
    @checkadmin
    def ajax_get_voucher(request):
        try:
            voucher_id = request.POST["voucher_id"]
            voucher_detail = list(Voucher.objects.filter(pk=voucher_id).values())
            context = {
                'voucher_detail': voucher_detail
            }
            return JsonResponse(context)
        except:
            messages.error(request, "Lấy dữ liệu mã giảm giá không thành công!")
            return redirect('ad_voucher')