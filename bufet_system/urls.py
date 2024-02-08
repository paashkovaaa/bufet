from django.urls import path

from bufet_system.views import index, MenuListView, ProductCartListView, RestaurantListView

urlpatterns = [
    path("", index, name="index"),
    path("menu/", MenuListView.as_view(), name="menu"),
    path("product_cart/", ProductCartListView.as_view(), name="product-cart"),
    path("restaurants/", RestaurantListView.as_view(), name="restaurant-list"),
]

app_name = "bufet_system"
