from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib import messages
from .forms import OrderForm, AddToCartForm
from .models import Dish, Restaurant, Order, User, ProductCart, ProductCartItem
from django.db import IntegrityError, transaction


class IndexView(View):
    def get(self, request):
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


class AddToCartView(LoginRequiredMixin, View):
    form_class = AddToCartForm
    success_url = reverse_lazy("bufet_system:product-cart")

    def post(self, request, dish_id):
        dish = get_object_or_404(Dish, pk=dish_id)
        cart, created = ProductCart.objects.get_or_create(user=request.user,
                                                          status="draft")
        quantity = int(request.POST.get("quantity", 1))
        cart.add_product(dish, quantity)
        messages.success(request, f"{dish.name} has been added to your cart.")
        return redirect(self.success_url)


class DeleteFromCartView(LoginRequiredMixin, View):
    model = ProductCartItem
    success_url = reverse_lazy("bufet_system:product-cart")

    def post(self, request, dish_id):
        dish = get_object_or_404(Dish, pk=dish_id)
        cart, created = (
            ProductCart.objects.get_or_create(user=request.user,
                                              status="draft"))
        quantity = int(request.POST.get("quantity", 1))

        cart.remove_product(dish, quantity)
        messages.success(request,
                         f"{dish.name} has been removed "
                         f"from your cart.")

        return redirect(self.success_url)


class ProductCartListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    context_object_name = "dishes"
    template_name = "bufet_system/product_cart.html"
    paginate_by = 5

    def get_queryset(self):
        try:
            cart = ProductCart.objects.get(user=self.request.user,
                                           status=ProductCart.STATUS_DRAFT)
            return cart.items.all()
        except ProductCart.DoesNotExist:
            return []

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            cart = ProductCart.objects.get(user=self.request.user,
                                           status=ProductCart.STATUS_DRAFT)
            context["total_price"] = cart.get_cart_total()
            quantities = {item.item_id: item.quantity for item
                          in cart.productcartitem_set.all()}
            context["quantities"] = quantities
            return context
        except ProductCart.DoesNotExist:
            return context


class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("bufet_system:menu")
    template_name = "bufet_system/order_checkout.html"

    def form_valid(self, form):
        user_product_carts = (
            ProductCart.objects.filter(user=self.request.user,
                                       status=ProductCart.STATUS_DRAFT))

        if user_product_carts.exists():
            cart = user_product_carts.first()
            form.instance.total_price = cart.get_cart_total()

            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.user = self.request.user
                    order.restaurant = form.cleaned_data["restaurant"]
                    order.product_cart = cart
                    order.save()

                    cart.status = ProductCart.STATUS_COMPLETED
                    cart.save()

                    return super().form_valid(form)
            except IntegrityError:
                messages.error(self.request,
                               "Error: There was an issue creating the order.")
                return redirect("bufet_system:menu")
        else:
            messages.error(self.request,
                           "Error: Your cart is empty. "
                           "Add items to your cart before placing an order.")
            return redirect("bufet_system:menu")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_product_carts = ProductCart.objects.filter(user=self.request.user,
                                                        status=ProductCart.STATUS_DRAFT)
        if user_product_carts.exists():
            cart = user_product_carts.first()
            context["total_price"] = cart.get_cart_total()
            context["dishes"] = cart.get_cart_items()
            quantities = {item.item_id: item.quantity for item
                          in cart.productcartitem_set.all()}
            context["quantities"] = quantities
        context["user_details"] = self.request.user
        context["restaurants"] = Restaurant.objects.all()
        return context


class DishDetailView(generic.DetailView):
    model = Dish
    template_name = "bufet_system/dish_detail.html"


class RestaurantListView(generic.ListView):
    model = Restaurant
    context_object_name = "restaurants"
    template_name = "bufet_system/restaurants.html"
    paginate_by = 10


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    context_object_name = "orders"
    template_name = "bufet_system/orders.html"
    paginate_by = 5
    login_url = "login"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user)
        else:
            return Order.objects.none()
