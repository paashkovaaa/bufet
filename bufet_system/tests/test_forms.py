from django.test import TestCase
from bufet_system.models import Restaurant
from bufet_system.forms import OrderForm, AddToCartForm


class OrderFormTest(TestCase):
    def test_order_form_valid_data(self):
        restaurant = Restaurant.objects.create(address="test address")
        data = {"restaurant": restaurant.id}
        form = OrderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_order_form_invalid_data(self):
        data = {}
        form = OrderForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("restaurant", form.errors)


class AddToCartFormTest(TestCase):
    def test_add_to_cart_form_valid_data(self):
        data = {"quantity": 2}
        form = AddToCartForm(data=data)
        self.assertTrue(form.is_valid())

    def test_add_to_cart_form_invalid_data(self):
        data = {"quantity": 0}
        form = AddToCartForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("quantity", form.errors)
