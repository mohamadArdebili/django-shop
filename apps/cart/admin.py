from django.contrib import admin
from . import models


class OrderItemAdmin(admin.TabularInline):
    model = models.OrderItem


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "is_paid"]
    inlines = [OrderItemAdmin]
    search_fields = ["is_paid", "user"]
    list_filter = ["is_paid", "user"]


@admin.register(models.Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ["name", "discount", "quantity"]
    list_filter = ["name", "discount"]
    search_fields = ["name"]
