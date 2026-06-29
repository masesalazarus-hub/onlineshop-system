from django.db import models
from orders.models import Order


class Payment(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    method = models.CharField(
        max_length=50
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    

class Payment(models.Model):

    PAYMENT_METHODS = (
        ('Cash', 'Cash'),
        ('M-Pesa', 'M-Pesa'),
        ('Tigo Pesa', 'Tigo Pesa'),
        ('Airtel Money', 'Airtel Money'),
        ('Bank', 'Bank'),
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHODS
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Payment #{self.id}"