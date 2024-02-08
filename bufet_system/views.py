from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from bufet_system.models import Restaurant, Order, User, Dish, ProductCart


def index(request: HttpRequest) -> HttpResponse:
    num_restaurants = Restaurant.objects.count()
    num_orders = Order.objects.count()
    num_users = User.objects.count()

    context = {
        "num_restaurants": num_restaurants,
        "num_orders": num_orders,
        "num_users": num_users

    }
    return render(request, "bufet_system/index.html", context=context)


class MenuListView(generic.ListView):
    model = Dish
    context_object_name = "dishes"
    template_name = "bufet_system/menu.html"
    paginate_by = 5


class ProductCartListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    context_object_name = "dishes"
    template_name = "bufet_system/product_cart.html"
    paginate_by = 5

    def get_queryset(self):
        try:
            cart = ProductCart.objects.get(user=self.request.user, status="draft")
            return cart.items.all()
        except ProductCart.DoesNotExist:
            # Redirect or handle empty cart case
            return Dish.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(ProductCart, user=self.request.user, status="draft")
        context["total_price"] = cart.get_cart_total()
        quantities = {item.dish_id: item.quantity for item in cart.productcartitem_set.all()}
        context["quantities"] = quantities
        return context


class RestaurantListView(generic.ListView):
    model = Restaurant
    restaurants = Restaurant.objects.all()
    context_object_name = "restaurants"
    template_name = "bufet_system/restaurants.html"
    paginate_by = 10
