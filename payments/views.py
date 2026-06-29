from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from orders.models import Order
from .models import Payment
@login_required
def make_payment(request, order_id):

    order = Order.objects.get(id=order_id)

    existing_payment = Payment.objects.filter(
        order=order
    ).first()

    if existing_payment:
        return redirect('receipt', order.id)

    if request.method == 'POST':

        method = request.POST['method']

        Payment.objects.create(
            order=order,
            amount=order.total_amount,
            method=method
        )

        order.status = 'Processing'
        order.save()

        return redirect('receipt', order.id)

    return render(
        request,
        'payments/payment.html',
        {'order': order}
    )

@login_required
def receipt(request, order_id):

    order = Order.objects.get(id=order_id)

    payment = Payment.objects.get(
        order=order
    )

    return render(
        request,
        'payments/receipt.html',
        {
            'order': order,
            'payment': payment
        }
    )