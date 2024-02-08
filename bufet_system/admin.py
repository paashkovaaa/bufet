from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from bufet_system.models import User, Dish, Restaurant, Order, ProductCart


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = UserAdmin.list_display + ("phone_number",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("phone_number",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("phone_number",)}),
    )


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "ingredients", "price", "weight")
    search_fields = ["name", ]
    list_filter = ["name", "price", "weight", ]


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("address",)
    search_fields = ["address"]
    list_filter = ["address", ]


@admin.register(ProductCart)
class ProductCartAdmin(admin.ModelAdmin):
    @admin.display(description="Items")
    def display_items(self, obj):
        return ", ".join([item.name for item in obj.items.all()])
    list_display = ("user", "created_at", "status", "display_items")
    search_fields = ["user__username"]
    list_filter = ["status"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    @admin.display(description="Dishes")
    def display_dishes(self, obj):
        return ", ".join([dish.name for dish in obj.dishes.all()])

    list_display = (
        "user", "restaurant", "created_at", "total_price", "display_dishes"
    )
    search_fields = ["user__username", "restaurant__address"]
    list_filter = ["user", "restaurant"]
