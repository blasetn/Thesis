from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from web.models import *
import os

from web.adminfile.context import *

class AccountUser:
    def signin(request):
        if 'signup' in request.POST:
            username = request.POST['signup_username']
            password = request.POST['signup_password']
            repassword = request.POST['signup_repassword']
            email = request.POST['signup_email']
            user_check = User.objects.filter(username=username)
            if user_check.count() < 1:
                if password == repassword:
                    user = User.objects.create_user(username, email, password)
                    user.save()
                    user_id = User.objects.get(pk=user.id)
                    UserDetail(user=user_id).save()
                    messages.success(request, "Đăng ký thành công!")
                else:
                    messages.error(request, "Đăng ký không thành công: Mật khẩu và nhập lại mật khẩu không khớp!")
            else:
                messages.error(request, "Đăng ký không thành công: Tài khoản đã tồn tại!")
        if 'signin' in request.POST:
            username = request.POST['signin_username']
            password = request.POST['signin_password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                messages.error(request, "Đăng nhập không thành công: Sai tài khoản hoặc mật khẩu!")
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'home/signin.html', context())


    def account(request):
        all_category = Category.objects.all()
        if request.user.is_authenticated:
            user_detail = UserDetail.objects.get(pk=request.user.id)
            dh = Order.objects.filter(user=request.user.id)
            if 'update' in request.POST:
                user_detail.ud_fullname = request.POST['fullname']
                user_detail.ud_sex = request.POST['sex']
                user_detail.ud_birthdate = request.POST['birthdate']
                user_detail.ud_phone = request.POST['phone']
                user_detail.ud_address = request.POST['address']
                if request.FILES.get('user_avatar', False):
                    try:
                        os.remove(user_detail.ud_avatar.path)
                    except:
                        pass
                    user_detail.ud_avatar = request.FILES['user_avatar']
                user_detail.save()
                user = User.objects.get(pk=request.user.id)
                user.email = request.POST['email']
                user.save()
                messages.success(request, "Cập nhật tài khoản thành công!")
                return redirect('account')
            if 'changepass' in request.POST:
                password_old = request.POST['password_old']
                password_new = request.POST['password_new']
                re_password_new = request.POST['re_password_new']
                user = authenticate(request, username=request.user.username, password=password_old)
                if user is not None:
                    if password_new == re_password_new:
                        user.set_password(password_new)
                        user.save()
                        messages.success(request, "Đổi mật khẩu thành công!")
                    else:
                        messages.error(request, "Đổi mật khẩu không thành công: Mật khẩu và nhập lại mật khẩu mới không khớp!")
                else:
                    messages.error(request, "Đổi mật khẩu không thành công: Mật khẩu cũ không đúng!")
                return redirect('account')
            return render(request, 'home/account.html', locals())
        else:
            return redirect('signin')


    def user_logout(request):
        logout(request)
        return redirect('home')