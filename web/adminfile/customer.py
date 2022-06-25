from django.contrib import messages
from django.shortcuts import redirect, render
from web.models import *
from django.http import JsonResponse
from web.adminfile.context import *
from django.contrib.auth.decorators import login_required
from web.decorators import *


class CustomerAdmin:
    @login_required(login_url='signin')
    @checkstaff
    def customer(request):
        all_customer = User.objects.filter(is_staff=False, is_superuser=False)
        print(all_customer)
        return render(request, 'admin/customer.html', locals())

    @login_required(login_url='signin')
    @checkstaff
    def ajax_get_order(request):
        try:
            user_id = request.POST["user"]
            order = list(Order.objects.filter(user=user_id).values())
            context = {
                'order': order,
            }
            return JsonResponse(context)
        except:
            messages.error(request, "Lỗi không tìm thấy được mục yêu cầu!")
            return redirect('customer')