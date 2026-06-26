from django.contrib import admin
from .models import UserData, Product, Order


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ("email","user","first_name", "last_name", "phone", "is_active", "created_at")
    search_fields = ("email", "first_name", "last_name", "phone")
    list_filter = ("is_active", "created_at")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)
    list_filter = ("price",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "old_customer_name",
        "product_name",
        "quantity",
        "price",
        "total",
        "payment_status",
        "order_date"
    )

    search_fields = (
        "product_name",
        "old_customer_name",
        "customer__username",
        "customer__first_name",
        "customer__last_name",
        "phone",
    )

    list_filter = ("payment_status", "order_date")
    ordering = ("-order_date",)
