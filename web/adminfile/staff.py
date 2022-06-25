from django.contrib import messages
from django.shortcuts import redirect, render
from web.models import *
from django.http import JsonResponse
from web.adminfile.context import *
from django.contrib.auth.decorators import login_required
from web.decorators import *


class StaffAdmin:
    @login_required(login_url='signin')
    @checkadmin
    def staff(request):
        all_staff = User.objects.filter(is_staff=True)
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            role = request.POST['role']
            email = request.POST['email']
            user_check = User.objects.filter(username=username)
            if user_check.count() < 1:
                user = User.objects.create_user(username, email, password)
                if role == '0':
                    user.is_superuser = True
                user.is_staff = True
                user.save()
                user_id = User.objects.get(pk=user.id)
                UserDetail(user=user_id).save()
                messages.success(request, "Thêm nhân viên thành công!")
            else:
                messages.error(request, "Tài khoản đã tồn tại!")
        return render(request, 'admin/staff.html', locals())

    def staff_update_role(request, id=None, func=None):
        try:
            staff = User.objects.get(pk=id)
            if func == 1:
                staff.is_superuser = True
            else:
                staff.is_superuser = False
            staff.save()
            messages.success(request, "Cập nhật nhân viên thành công!")
        except:
            messages.error(request, "Lỗi! Không tìm thấy nhân viên này!")
        return redirect('staff')
