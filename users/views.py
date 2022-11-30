from django.shortcuts import render
from .serializers import UserRegisterSerializer, User, UserSerializer
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response



@api_view(["GET"])
def userProfile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(["POST"])
def registration(request):
    serializer = UserRegisterSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data["username"] = account.username
        data["email"] = account.email
        refresh = RefreshToken.for_user(account)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

    else:
        data["errors"] = serializer.errors

    return Response(data)




