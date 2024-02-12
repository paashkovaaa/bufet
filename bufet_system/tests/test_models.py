from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from bufet_system.models import (Dish,
                                 Restaurant,
                                 ProductCart,
                                 ProductCartItem,
                                 Order)


class UserModelTest(TestCase):
    def test_user_str_representation(self):
        user = get_user_model().objects.create_user(
            username="testuser",
            first_name="John",
            last_name="Doe")
        self.assertEqual(str(user), "testuser (John Doe)")


class DishModelTest(TestCase):
    def test_dish_str_representation(self):
        dish = Dish(name="Test Dish",
                    ingredients="Ingredient 1, Ingredient 2",
                    price=10.99,
                    weight=250.0)
        self.assertEqual(str(dish), "Test Dish: 10.99 uah (250.0 g)")


class RestaurantModelTest(TestCase):
    def test_restaurant_str_representation(self):
        restaurant = Restaurant(address="Test Address")
        self.assertEqual(str(restaurant), "Restaurant: Test Address")


class ProductCartModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser",
            phone_number="123456789")
        self.dish1 = Dish.objects.create(name="Dish 1",
                                         ingredients="Ingredient 1",
                                         price=Decimal('10.99'),
                                         weight=Decimal(200.00))
        self.dish2 = Dish.objects.create(name="Dish 2",
                                         ingredients="Ingredient 1",
                                         price=Decimal('12.99'),
                                         weight=Decimal(500.00))
        self.cart = ProductCart.objects.create(user=self.user)
        self.restaurant = Restaurant.objects.create(address="Test Address")

    def test_product_cart_str_representation(self):
        self.assertEqual(str(self.cart), f"product cart: {self.cart.id}")

    def test_add_and_remove_from_cart(self):
        initial_items_count = self.cart.get_cart_items().count()
        self.cart.add_product(self.dish1)
        self.assertEqual(self.cart.get_cart_items().count(),
                         initial_items_count + 1)
        self.cart.remove_product(self.dish1)
        self.assertEqual(self.cart.get_cart_items().count(), 0)

    def test_update_quantity(self):
        self.cart.add_product(self.dish1)
        self.assertEqual(self.cart.get_cart_total(), self.dish1.price)
        self.cart.update_quantity(self.dish1, 2)
        cart_item = self.cart.productcartitem_set.get(item=self.dish1)
        self.assertEqual(self.cart.get_cart_total(), self.dish1.price * 2)
        self.assertEqual(cart_item.quantity, 2)

    def test_create_order(self):
        self.cart.add_product(self.dish1)
        self.cart.add_product(self.dish2)
        self.cart.create_order(restaurant=self.restaurant)
        order = Order.objects.first()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.restaurant, self.restaurant)
        self.assertEqual(order.total_price, self.cart.get_cart_total())


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser",
            phone_number="123456789")
        self.cart = ProductCart.objects.create(user=self.user)
        self.order = Order.objects.create(user=self.user,
                                          total_price=20.0,
                                          product_cart=self.cart)

    def test_order_str_representation(self):
        expected_str = (f"Id: {self.order.id}, "
                        f"{self.order.product_cart}, "
                        f"user: {self.user.username}, "
                        f"total price: 20.0")
        self.assertEqual(str(self.order), expected_str)


class ProductCartItemModelTest(TestCase):
    def test_product_cart_item_creation(self):
        user = get_user_model().objects.create(
            username="testuser",
            phone_number="123456789")
        product_cart = ProductCart.objects.create(user=user)
        dish = Dish.objects.create(name="Test Dish",
                                   ingredients="Ingredient 1",
                                   price=9.99,
                                   weight=200.0)

        product_cart_item = ProductCartItem.objects.create(cart=product_cart,
                                                           item=dish,
                                                           quantity=2)

        self.assertEqual(product_cart_item.cart, product_cart)
        self.assertEqual(product_cart_item.item, dish)
        self.assertEqual(product_cart_item.quantity, 2)
