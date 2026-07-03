from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Cart
from products.models import Product

@login_required
def add_to_cart(request, product_id):

    product = Product.objects.get(id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

@login_required
def cart_view(request):

    items = Cart.objects.filter(
        user=request.user
    )

    total = 0

    for item in items:
        total += item.product.price * item.quantity

    return render(
        request,
        'cart/cart.html',
        {
            'items': items,
            'total': total
        }
    )
@login_required
def increase_quantity(request, cart_id):

    item = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    item.quantity += 1
    item.save()

    return redirect('cart')
@login_required
def decrease_quantity(request, cart_id):

    item = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()

    return redirect('cart')

@login_required
def remove_item(request, cart_id):

    item = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    item.delete()

    return redirect('cart')