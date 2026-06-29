from django.urls import path
from . import views

urlpatterns = [

    path(
        'payment/<int:order_id>/',
        views.make_payment,
        name='payment'
    ),

    path(
        'receipt/<int:order_id>/',
        views.receipt,
        name='receipt'
    ),

]