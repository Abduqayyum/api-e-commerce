from django.urls import path
from .views import *

urlpatterns = [
    path("products/", getProducts, name="products"),
    path("users/profile/", userProfile, name="user-profile"),
    path("users/profile-update/", updateUserProfile, name="update-user-profile"),
    path("users/", getUsers, name="users"),
    path("add-order-items/", addOrderItems, name="add-order-items"),
    path("<int:pk>/", getOrderById, name="user-order"),
    path("<int:id>/delivered/", updateOrderToDelivered, name="update-to-delivered"),
    path("myorders/", myOrders, name="myorders"),
    path("delete-user/", deleteUser, name="delete-user"),
    path("user/<int:pk>/", getUserById, name="get-user"),
    path("product-delete/<int:pk>", deleteProduct, name="delete-product"),
    path("product-create/", createProduct, name="product-create"),
    path("product-update/<int:pk>/", updateProduct, name="update-create"),
    path("products/<int:pk>/", getProduct, name="product-detail"),
    path("<int:pk>/reviews/", createProductReview, name="review-create"),
    path("top-products/", getTopProducts, name="top-products")
]
