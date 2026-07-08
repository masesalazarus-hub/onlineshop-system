from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from orders.models import Order
from payments.models import Payment


@login_required
def dashboard(request):

    orders = Order.objects.filter(customer=request.user)
    payments = Payment.objects.filter(order__customer=request.user)

    recent_orders = orders.order_by('-created_at')[:5]

    total_spent = orders.aggregate(
        Sum('total_amount')
    )['total_amount__sum'] or 0

    context = {
        'total_orders': orders.count(),
        'total_payments': payments.count(),
        'total_spent': total_spent,
        'recent_orders': recent_orders,
    }

    return render(
        request,
        'customer/dashboard.html',
        context
    )