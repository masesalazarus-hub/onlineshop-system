from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Sum
from orders.models import OrderItem
from products.models import Product
from orders.models import Order
from payments.models import Payment
from django.http import HttpResponse
import openpyxl
from django.contrib.auth.decorators import login_required, user_passes_test
def admin_required(user):
    return user.is_superuser
@login_required
@user_passes_test(admin_required)
def dashboard(request):

    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_customers = User.objects.count()

    revenue = Payment.objects.aggregate(
        Sum('amount')
    )['amount__sum'] or 0
    best_products = (
    OrderItem.objects
    .values('product__name')
    .annotate(total_sold=Sum('quantity'))
    .order_by('-total_sold')[:5]
)

    return render(
        request,
        'dashboard/dashboard.html',
        {
            'products': total_products,
            'orders': total_orders,
            'customers': total_customers,
            'revenue': revenue,
            'best_products': best_products,
        }
    )
@login_required
@user_passes_test(admin_required)
def reports(request):

    orders = Order.objects.all().order_by('-id')

    return render(
        request,
        'dashboard/reports.html',
        {
            'orders': orders
        }
    )
@login_required
@user_passes_test(admin_required)
def export_excel(request):

    workbook = openpyxl.Workbook()

    sheet = workbook.active

    sheet.title = "Orders"

    sheet.append([
        "Order ID",
        "Customer",
        "Amount",
        "Status"
    ])

    orders = Order.objects.all()

    for order in orders:

        sheet.append([
            order.id,
            order.customer.username,
            order.total_amount,
            order.status
        ])

    response = HttpResponse(
        content_type=
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename=orders.xlsx'

    workbook.save(response)

    return response
@login_required
@user_passes_test(admin_required)
def manage_orders(request):

    orders = (
        Order.objects
        .select_related('customer')
        .order_by('-created_at')
    )

    return render(
        request,
        'dashboard/manage_orders.html',
        {
            'orders': orders
        }
    )

@login_required
@user_passes_test(admin_required)
def update_order_status(request, order_id, status):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if status in [
        'Pending',
        'Processing',
        'Delivered'
    ]:
        order.status = status
        order.save()

    return redirect('manage_orders')
@login_required
@user_passes_test(admin_required)
def order_details(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    items = OrderItem.objects.filter(
        order=order
    )

    payment = Payment.objects.filter(
        order=order
    ).first()

    return render(
        request,
        'dashboard/order_details.html',
        {
            'order': order,
            'items': items,
            'payment': payment,
        }
    )