from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from cart.models import Cart
from .models import Order, OrderItem
from django.shortcuts import render

@login_required
def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items:
        return redirect('cart')

    # Hakikisha stock inatosha
    for item in cart_items:
        if item.quantity > item.product.stock:
            return redirect('cart')

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    order = Order.objects.create(
        customer=request.user,
        total_amount=total
    )

    for item in cart_items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

        # Punguza stock
        item.product.stock -= item.quantity
        item.product.save()

    cart_items.delete()

    return redirect('payment', order.id)

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        customer=request.user
    ).order_by('-id')

    return render(
        request,
        'orders/my_orders.html',
        {
            'orders': orders
        }
    )