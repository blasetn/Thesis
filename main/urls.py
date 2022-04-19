from django.conf import settings
from django.contrib import admin
from django.urls import path
from web import views
from django.conf.urls.static import static

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    path('home/signin', views.signin, name='signin'),
    path('home/signup', views.signup, name='signup'),
    path('home/account', views.account, name='account'),
    path('home/cart', views.cart, name='cart'),
    path('home/checkout', views.checkout, name='checkout'),
    path('home/about', views.about, name='about'),
    path('home/blog', views.blog, name='blog'),
    path('home/blogdetail', views.blogdetail, name='blogdetail'),
    path('home/contact', views.contact, name='contact'),
    path('home/shop', views.shop, name='shop'),
    path('home/product', views.product, name='product'),
    path('home/search', views.search, name='search'),
    # Admin
    path('admin/', views.admin, name='admin'),
    path('admin/category/', views.category, name='category'),
    path('admin/category/<int:id>', views.category, name='category'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
