from django.urls import path

from bufet_system.views import (MenuListView,
                                ProductCartListView,
                                OrderCreateView,
                                DishDetailView,
                                RestaurantListView,
                                AddToCartView,
                                DeleteFromCartView, OrderListView, IndexView)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("menu/", MenuListView.as_view(), name="menu"),
    path("product_cart/", ProductCartListView.as_view(), name="product-cart"),
    path("checkout/", OrderCreateView.as_view(), name="order-checkout"),
    path("dish/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("delete-from-cart/<int:dish_id>/",
         DeleteFromCartView.as_view(),
         name="delete-from-cart"),
    path("restaurants/", RestaurantListView.as_view(), name="restaurant-list"),
    path("add-to-cart/<int:dish_id>/",
         AddToCartView.as_view(),
         name="add-to-cart"),
    path("orders/", OrderListView.as_view(), name="order-list")
]

app_name = "bufet_system"
