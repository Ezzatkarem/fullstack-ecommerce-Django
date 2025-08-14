from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:pk>/<str:action>/', views.cart_update, name='cart_update'),
    path('remove/<int:pk>/', views.cart_remove, name='cart_remove'),
]
