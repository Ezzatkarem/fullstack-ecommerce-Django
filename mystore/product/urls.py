from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),  # الصفحة الرئيسية تعرض المنتجات
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/create/', views.product_create, name='product_create'),
    path('product/<slug:slug>/edit/', views.product_edit, name='product_edit'),
    path('product/<slug:slug>/delete/', views.product_delete, name='product_delete'),
]
