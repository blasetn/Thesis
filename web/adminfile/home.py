from django.shortcuts import render

class HomeAdmin:
    def admin(request):
        return render(request, 'admin/index.html')