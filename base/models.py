from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products", null=True, blank=True)
    name = models.CharField(max_length=60, null=True, blank=True)
    image = models.ImageField(upload_to="images", null=True, blank=True)
    brand = models.CharField(max_length=60, null=True, blank=True)
    category = models.CharField(max_length=60, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    countInStock = models.IntegerField(default=0, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, related_name="review_product", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, related_name="review_user",on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, related_name="order_user",on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, related_name="order_product", on_delete=models.CASCADE, null=True, blank=True)
    paymentMethod = models.CharField(max_length=200, blank=True, null=True)
    taxPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(auto_now_add=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

class OrdetItem(models.Model):
    user = models.ForeignKey(User, related_name="orderitem_user",on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, related_name="orderitem_product", on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, related_name="orderitems", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="images", null=True, blank=True)
    qty = models.IntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.product.name


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True, related_name="shipping_order")
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    shippingPrice = models.DecimalField(decimal_places=2, max_digits=7 , null=True, blank=True)

    def __str__(self):
        return self.order.product.name


