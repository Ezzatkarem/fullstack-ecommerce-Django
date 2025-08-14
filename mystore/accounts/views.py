from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProfileForm
from .models import UserProfile 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from cart.models import CartItem, Cart
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from cart.models import CartItem
from django.conf import settings

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            if password != password2:
                form.add_error('password2', "Passwords do not match")
            else:
                user = form.save(commit=False)
                user.set_password(password)
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                login(request, user)
                return redirect('frontpage')
    else:
        form = RegisterForm()
        profile_form = ProfileForm()

    context = {'form': form, 'profile_form': profile_form}
    return render(request, 'accounts/register.html', context)

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('frontpage')
        else:
            error = 'Invalid username or password'
    return render(request, 'accounts/login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('frontpage')


@login_required(login_url='login')
def profile_view(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    purchased_items = CartItem.objects.filter(cart__user=request.user, cart__ordered=True)

    # أضف حقل subtotal لكل عنصر
    for item in purchased_items:
        item.subtotal = item.product.price * item.quantity

    total = sum(item.subtotal for item in purchased_items)

    context = {
        'profile': profile,
        'purchased_items': purchased_items,
        'total': total,
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, 'accounts/profile.html', context)
