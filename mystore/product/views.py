from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseForbidden
from .models import Product, Category
from .forms import ProductForm

def product_list(request):
    category_slug = request.GET.get('category', '')
    q = request.GET.get('q', '')

    categories = Category.objects.all()
    products = Product.objects.all()

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if q:
        products = products.filter(name__icontains=q)

    context = {
        'products': products,
        'categories': categories,
        'active_category': category_slug,
        'search_query': q,
    }
    return render(request, 'product/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product/product_detail.html', {'product': product})


def is_staff(user):
    return user.is_active and user.is_staff

@user_passes_test(is_staff)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product/product_form.html', {'form': form, 'create': True})


@user_passes_test(is_staff)
def product_edit(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', slug=product.slug)
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/product_form.html', {'form': form, 'create': False})


@user_passes_test(is_staff)
def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product/product_confirm_delete.html', {'product': product})
