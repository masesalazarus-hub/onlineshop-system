from django.urls import path
from . import views

urlpatterns = [
    # Customer
    path('products/', views.product_list, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Admin Products
    path('dashboard/products/', views.admin_products, name='admin_products'),
    path('dashboard/products/add/', views.add_product, name='add_product'),
    path('dashboard/products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('dashboard/products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
]