from django.db import models
from django.conf import settings
from product.models import Product  # لو عندك تطبيق المنتجات اسمه product
from django.contrib.auth.models import User  # <-- أضف السطر ده

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
