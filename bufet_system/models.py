from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Dish(models.Model):
    name = models.CharField(max_length=150)
    ingredients = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Dishes"

    def __str__(self):
        return f"{self.name}: {self.price} uah ({self.weight} g)"


class Restaurant(models.Model):
    address = models.TextField()

    class Meta:
        ordering = ("address",)

    def __str__(self):
        return f"Restaurant: {self.address}"


class ProductCartItem(models.Model):
    cart = models.ForeignKey("ProductCart", on_delete=models.CASCADE)
    item = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class ProductCart(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_COMPLETED = "completed"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_COMPLETED, "Completed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default=STATUS_DRAFT)
    items = models.ManyToManyField(Dish,
                                   through=ProductCartItem,
                                   related_name="dishes")

    def __str__(self):
        return f"product cart: {self.id}"

    def get_cart_items(self):
        return self.items.all()

    def create_order(self, restaurant=None):
        order = Order.objects.create(
            user=self.user,
            restaurant=restaurant,
            total_price=self.get_cart_total()
        )
        self.order = order
        self.status = self.STATUS_COMPLETED
        self.save()

    def get_cart_total(self):
        return sum(
            [item.item.price *
             item.quantity for item
             in self.productcartitem_set.all()]
        )

    def add_product(self, item, quantity=1):
        existing_item, created = (
            self.productcartitem_set.get_or_create(item=item))
        if not created:
            existing_item.quantity += quantity
            existing_item.save()

    def remove_product(self, item, quantity=1):
        existing_item, created = (
            self.productcartitem_set.get_or_create(item=item))
        if not created:
            existing_item.quantity -= quantity
            if existing_item.quantity <= 0:
                existing_item.delete()
            else:
                existing_item.save()

    def update_quantity(self, item, quantity):
        cart_item, created = self.productcartitem_set.get_or_create(item=item)
        if not created:
            cart_item.quantity = quantity
            cart_item.save()


class Order(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="order")
    restaurant = models.ForeignKey(Restaurant,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True,
                                   related_name="order")
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_cart = models.OneToOneField(ProductCart,
                                        on_delete=models.CASCADE,
                                        null=True,
                                        blank=True,
                                        related_name="order")

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return (f"Id: {self.id}, {self.product_cart}, "
                f"user: {self.user.username}, "
                f"total price: {self.total_price}")

    def get_cart_items(self):
        return self.product_cart.items.all()

    def get_cart_total(self):
        return sum(
            [item.item.price *
             item.quantity for item
             in self.product_cart.productcartitem_set.all()]
        )
