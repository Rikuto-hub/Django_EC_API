from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Category, Product, CartItem, Order

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id','email','password')
        extra_kwargs= {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model = Profile
        fields = ('id', 'nickName', 'address_num', 'address_str', 'created_on', 'userProfile')
        extra_kwargs = {'userProfile': {'read_only': True}}

class CategorySerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model = Category
        fields = ("id", "title", "created_on")

class ProductGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ("id", "title", "description", 'created_on', "category")

class ProductPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "title", "description", 'created_on', "category")

# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers. CharField(max_length=50)
#     description = serializers.CharField(max_length=100)
#     created_on = serializers.DateField()
#     category = serializers.ForeignKey(Category, on_delete=models.CASCADE)

#     def create(self, validated_data):
#         return Product(**validated_data)

#     def update(self, instance, validated_data):
#         instance.id = validated_data.get('id', instance.id)
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.created_on = validated_data.get('created_on', instance.created_on)
#         instance.category = validated_data.get('category', instance.category)
#         return instance

class CartItemGetSerializer(serializers.ModelSerializer):
    product = ProductGetSerializer()
    class Meta:
        model = CartItem
        fields = ("id", "user", "product", "payment", "quantity")
        extra_kwargs = {'user': {'read_only': True}}

class CartItemPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("id", "user", "product", "payment", "quantity")
        extra_kwargs = {'user': {'read_only': True}}

class OrderGetSerializer(serializers.ModelSerializer):
    products = ProductGetSerializer(many=True)
    class Meta:
        model = Order
        fields = ("id", "user", "products")

class OrderPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "user", "products")