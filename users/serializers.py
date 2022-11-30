from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})
    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]

    def save(self):
        password = self.validated_data.get("password")
        password2 = self.validated_data.get("password2")
        email = self.validated_data.get("email")
        username = self.validated_data.get("username")

        if password != password2:
            raise serializers.ValidationError({"error": "P1 and P2 should be same!"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "Email already exists!"})

        account = User(email=email, username=username)
        account.set_password(password)
        account.save()
        return account


class UserSerializer(serializers.ModelSerializer):
    name =  serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "email", "name", "isAdmin"]

    def get_name(self, obj):
        name = obj.first_name
        if name == "":
            name = obj.email
        return name


    def get_isAdmin(self, obj):
        return obj.is_staff