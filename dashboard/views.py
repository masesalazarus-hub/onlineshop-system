from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Sum
from orders.models import OrderItem
from products.models import Product
from orders.models import Order
from payments.models import Payment
from django.http import HttpResponse
import openpyxl


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
def reports(request):

    orders = Order.objects.all().order_by('-id')

    return render(
        request,
        'dashboard/reports.html',
        {
            'orders': orders
        }
    )
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