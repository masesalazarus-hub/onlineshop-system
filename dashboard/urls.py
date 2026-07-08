from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reports/', views.reports, name='reports'),
    path('export-excel/',views.export_excel,name='export_excel'),
    path(
    'manage-orders/',
    views.manage_orders,
    name='manage_orders'
),

path(
    'order/<int:order_id>/<str:status>/',
    views.update_order_status,
    name='update_order_status'
),
path(
    'order-details/<int:order_id>/',
    views.order_details,
    name='order_details'
),
]