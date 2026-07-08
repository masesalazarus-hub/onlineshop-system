from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='products'),
    path('product/<int:product_id>/',views.product_detail,name='product_detail'),
path(
    'admin/products/',
    views.admin_products,
    name='admin_products'
),

path(
    'admin/products/add/',
    views.add_product,
    name='add_product'
),
path(
        'admin/products/edit/<int:product_id>/',
        views.edit_product,
        name='edit_product'
    ),

    path(
        'admin/products/delete/<int:product_id>/',
        views.delete_product,
        name='delete_product'
    ),
]