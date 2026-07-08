from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from urllib.parse import quote

from orders.models import Order
from .models import Payment


@login_required
def make_payment(request, order_id):

    order = Order.objects.get(id=order_id)

    existing_payment = Payment.objects.filter(order=order).first()

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
        {
            'order': order
        }
    )


@login_required
def receipt(request, order_id):

    order = Order.objects.get(id=order_id)

    payment = Payment.objects.get(order=order)

    return render(
        request,
        'payments/receipt.html',
        {
            'order': order,
            'payment': payment
        }
    )


@login_required
def send_whatsapp(request, order_id):

    order = Order.objects.get(id=order_id)
    payment = Payment.objects.get(order=order)

    phone = "255628759508"

    message = f"""
🛒 NEW ORDER

Order ID: {order.id}

Amount: TZS {order.total_amount}

Payment Method: {payment.method}

Customer has completed payment.

Please verify the payment.
"""

    whatsapp_url = (
        f"https://wa.me/{phone}?text={quote(message)}"
    )

    return redirect(whatsapp_url)