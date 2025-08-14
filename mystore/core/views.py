from django.shortcuts import render
from product.models import Product, Category
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from product.models import Product, Category

def frontpage(request):
    categories = Category.objects.all()
    
    if request.user.is_authenticated:
        products = Product.objects.all().order_by('-created_at')[:8]
    else:
        products = Product.objects.none()  # مش هتظهر أي منتجات

    return render(request, 'core/frontpage.html', {
        'products': products,
        'categories': categories
    })

@login_required(login_url='accounts:login')
def shop(request):
    category_slug = request.GET.get('category', '')
    search_query = request.GET.get('q', '')

    categories = Category.objects.all()
    products = Product.objects.all()

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if search_query:
        products = products.filter(name__icontains=search_query)

    context = {
        'categories': categories,
        'products': products,
        'active_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'core/shop.html', context)
@login_required(login_url='accounts:login')
def contact_view(request):
    return render(request, 'core/contact.html')