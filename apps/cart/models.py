from django.db import models
from apps.account.models import User
from apps.product.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.phone


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="items")
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    quantity = models.PositiveSmallIntegerField()
    price = models.PositiveSmallIntegerField()


class Discount(models.Model):
    name = models.CharField(max_length=20)
    discount = models.PositiveSmallIntegerField(default=0, unique=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name
