from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from django.shortcuts import render

from product.models import Product

@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart:cart_detail')


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    
    cart_items = []
    total = 0
    for item in items:
        subtotal = item.product.price * item.quantity
        total += subtotal
        cart_items.append({
            'id': item.pk,        # هنا ضيف السطر
            'product': item.product,
            'quantity': item.quantity,
            'subtotal': subtotal,
        })
    
    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total': total,
    })

from django.urls import reverse

@login_required
def cart_update(request, pk, action):
    try:
        item = CartItem.objects.get(pk=pk, cart__user=request.user)
    except CartItem.DoesNotExist:
       return redirect('cart:cart_detail')
  # صححنا هنا

    if action == 'increase':
        item.quantity += 1
        item.save()
    elif action == 'decrease' and item.quantity > 1:
        item.quantity -= 1
        item.save()
    return redirect('cart:cart_detail')
  # صححنا هنا


@login_required
def cart_remove(request, pk):
    try:
        item = CartItem.objects.get(pk=pk, cart__user=request.user)
        item.delete()
    except CartItem.DoesNotExist:
        pass  # لو مش موجود، تجاهل
    return redirect('cart:cart_detail')

