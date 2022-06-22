from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from web.decorators import *

class HomeAdmin:
    @login_required(login_url='signin')
    @checkstaff
    def admin(request):
        return render(request, 'admin/index.html')