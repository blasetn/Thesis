from django.conf import settings
from django.contrib import admin
from django.urls import path
from web import views
from django.conf.urls.static import static

urlpatterns = [
    #Home
    path('', views.HomeUser.home, name='home'),
    path('home/', views.HomeUser.home, name='home'),
    path('home/signin/', views.AccountUser.signin, name='signin'),
    path('home/logout/', views.AccountUser.user_logout, name='logout'),
    path('home/account/', views.AccountUser.account, name='account'),
    path('home/cart/', views.OrderUser.cart, name='cart'),
    path('home/action_cart/', views.OrderUser.action_cart, name='action_cart'),
    path('home/checkout/', views.OrderUser.checkout, name='checkout'),
    path('home/order_detail/<int:id>/', views.OrderUser.order_detail, name='order_detail'),
    path('home/shop/', views.ProductUser.shop, name='shop'),
    path('home/shop/<int:id>/', views.ProductUser.shop, name='shop'),
    path('home/product/<int:id>/', views.ProductUser.product, name='product'),
    path('home/search/', views.ProductUser.search, name='search'),
    # Admin
    path('admin/', views.HomeAdmin.admin, name='admin'),
    path('admin/category/', views.CategoryAdmin.category, name='ad_category'),
    path('admin/ajax_get_category/', views.CategoryAdmin.ajax_get_category, name='ajax_get_category'),
    path('admin/brand/', views.BrandAdmin.ad_brand, name='ad_brand'),
    path('admin/ajax_get_brand/', views.BrandAdmin.ajax_get_brand, name='ajax_get_brand'),
    path('admin/product/', views.ProductAdmin.ad_product, name='ad_product'),
    path('admin/ajax_get_product/', views.ProductAdmin.ajax_get_product, name='ajax_get_product'),
    path('admin/voucher/', views.VoucherAdmin.voucher, name='ad_voucher'),
    path('admin/ajax_get_voucher/', views.VoucherAdmin.ajax_get_voucher, name='ajax_get_voucher'),
    path('admin/chat/', views.ChatAdmin.chat, name='ad_chat'),

    path(r'vnpay', views.index, name='index'),
    path(r'payment', views.payment, name='payment'),
    path(r'payment_return', views.OrderUser.payment_return, name='payment_return'),
    # path(r'query', views.query, name='query'),
    # path(r'refund', views.refund, name='refund'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)