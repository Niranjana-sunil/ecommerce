from .models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class ProductImageSerializer(serializers.ModelSerializer):
    image=serializers.SerializerMethodField()

    class Meta:
        model=ProductImage
        fields=[
            "image",
        ]

        read_only_fields=[
            "id",
            "created_at",
        ]

    def get_image(self,obj):
        if not obj.image:
            return None
        return obj.image.url


class ProductSerializer(serializers.ModelSerializer):
    images=ProductImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model=Product
        fields=[
            "id",
            "name",
            "description",
            "price",
            "images",
            "created_at",
            "updated_at",
        ]

        read_only_fields=[
            "id",
            "images",
            "created_at",
            "updated_at",
        ]

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        fields ='__all__'
    def create(self, validated_data):
        validated_data["password"] = make_password(
            validated_data["password"]
        )

        return Users.objects.create(**validated_data)


class AdminLoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(
        write_only=True
        )


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name",read_only=True)

    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    product_images = ProductImageSerializer(
        source="product.images",
        many=True,
        read_only=True
    )

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            "quantity",
            "product_images",
        ]


class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model=Cart
        fields=[
            "id",
            "user",
            "items",
            "created_at",
            "updated_at"
        ]


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = "__all__"



class OrderSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Order
        fields = "__all__"


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id", "username", "phone", "email"]





