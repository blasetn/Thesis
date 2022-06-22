from django.http import HttpResponse


def checkstaff(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('Bạn không đủ quyền truy cập.')
    return wrapper_func


def checkadmin(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('Bạn không đủ quyền truy cập.')
    return wrapper_func


# def chapnhan(allowed_roles=[]):
#     def decorator(view_func):
#         def wrapper_func(request, *args, **kwargs):
#             group = None
#             if request.user.groups.exists():
#                 group = request.user.groups.all()[0].name
#             if group in allowed_roles or request.user.is_superuser:
#                 return view_func(request, *args, **kwargs)
#             else:
#
#         return wrapper_func
#     return decorator
