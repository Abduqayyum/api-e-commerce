from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.serializers import UserSerializer
from rest_framework import status
import datetime
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage

# Create your views here.



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def userProfile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(["PUT"])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializer(data=request.data, instance=user)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        return Response({"error": serializer.errors})


@api_view(["GET"])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProducts(request):
    query = request.query_params.get("keyword")
    if query == None:
        query = ""
    products = Product.objects.filter(name__icontains=query)

    page = request.query_params.get("page")
    paginator = Paginator(products, 2)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    serializer = ProductSerializer(products, many=True)
    return Response({"products": serializer.data, "page": page, "pages": paginator.num_pages})


@api_view(["GET"])
def getTopProducts(request):
    products = Product.objects.filter(rating_gte=4).order_by("-rating")[0:6]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProduct(request, pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(["DELETE"])
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return Response("Product was deleted!")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data
    orderItems = data["orderItems"]

    if orderItems and len(orderItems) == 0:
        return Response({"detail": "No order items"}, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        order = Order.objects.create(
            user=user,
            paymentMethod=data["paymentMethod"],
            taxPrice=data["taxPrice"],
            shippingPrice=data["shippingPrice"],
            totalPrice=data["totalPrice"]
        )

        shippingAddress = ShippingAddress.objects.create(
            address=data["shippingAddress"]["address"],
            order=order,
            city=data['shippingAddress']["city"],
            postalCode=data['shippingAddress']["postalCode"],
            country=data['shippingAddress']["country"],
        )

        for i in orderItems:
            product = Product.objects.get(id=i['product'])

            item = OrdetItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i["qty"],
                price=i["price"],
                image=product.image.url
            )

            product.countInStock -= item.qty
            product.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    user = request.user

    try:
        order = Order.objects.get(id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            return Response({"detail": "Not authorized to view this order"}, status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response({"detail": "Order does not exist"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def myOrders(request):
    user = request.user
    orders = user.order_user.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return Response("User was deleted!")


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def createProduct(request):
    user = request.user
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    product = Product.objects.get(id=pk, user=request.user)
    serializer = ProductSerializer(data=request.data, instance=product)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request, pk):
    order = Order.objects.get(id=pk)
    order.isDelivered = True
    order.deliveredAt = datetime.now()
    order.save()
    return Response("Order was delivered")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    user = request.user
    product = Product.objects.get(id=pk)
    data = request.data
    already_exist = product.review_product.filter(user=user).exists()
    if already_exist:
        return Response({"detail": "You have already reviewed this product"})
    elif data["rating"] == 0:
        return Response({"detail": "Please select a rating"})
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.username,
            rating=data["rating"],
            comment=data["comment"]
        )

        reviews = product.review_product.all()
        product.numReviews = len(reviews)
        total = 0
        for i in reviews:
            total += i.rating

        product.rating = total / len(reviews)
        product.save()

        return Response("Review added")


