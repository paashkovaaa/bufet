from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from bufet_system.models import (Dish,
                                 Restaurant,
                                 Order,
                                 ProductCart,
                                 ProductCartItem)


class BufetSystemViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            phone_number="123456789")

        self.restaurant = Restaurant.objects.create(address="Test Address")

        self.dish = Dish.objects.create(name="Dish",
                                        ingredients="Ingredient 1",
                                        price=9.99,
                                        weight=200.0
                                        )

    def test_index_view(self):
        response = self.client.get(reverse("bufet_system:index"))
        self.assertEqual(response.status_code, 200)

    def test_menu_list_view(self):
        response = self.client.get(reverse("bufet_system:menu"))
        self.assertEqual(response.status_code, 200)

    def test_restaurant_list_view(self):
        response = self.client.get(reverse("bufet_system:restaurant-list"))
        self.assertEqual(response.status_code, 200)

    def test_dish_detail_view(self):
        url = reverse("bufet_system:dish-detail", kwargs={'pk': self.dish.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["dish"], self.dish)

    def test_product_cart_list_view(self):
        self.client.force_login(self.user)
        cart = ProductCart.objects.create(user=self.user, status="draft")
        ProductCartItem.objects.create(cart=cart, item=self.dish, quantity=2)
        response = self.client.get(reverse('bufet_system:product-cart'))
        self.assertEqual(response.status_code, 200)

    def test_order_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("bufet_system:order-list"))
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse(
            "bufet_system:add-to-cart",
            args=[self.dish.id]),
            {"quantity": 2})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProductCart.objects.count(), 1)
        self.assertEqual(ProductCartItem.objects.count(), 1)

    def test_delete_from_cart_view(self):
        self.client.force_login(self.user)
        cart = ProductCart.objects.create(user=self.user, status="draft")
        item = ProductCartItem.objects.create(cart=cart,
                                              item=self.dish,
                                              quantity=1)
        response = self.client.post(reverse("bufet_system:delete-from-cart",
                                            args=[self.dish.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProductCartItem.objects.count(), 0)

    def test_order_create_view_with_cart(self):
        self.client.force_login(self.user)
        cart = ProductCart.objects.create(user=self.user)
        ProductCartItem.objects.create(cart=cart, item=self.dish, quantity=2)
        response = self.client.post(reverse("bufet_system:order-checkout"),
                                    {"restaurant": self.restaurant.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(ProductCart.objects.get(id=cart.id).status,
                         ProductCart.STATUS_COMPLETED)
