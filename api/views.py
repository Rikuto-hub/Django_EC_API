from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from .models import Profile, Category, Product, CartItem, Order
from . import serializers

class ProfileListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.filter(userProfile=self.request.user.id)
        serializer = serializers.ProfileSerializer(profile, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = serializers.ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryListCreateAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        categories = Category.objects.prefetch_related('products').all()
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            serializer = serializers.CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        category = get_object_or_404(Category, pk=pk)
        return category

    def get(self, request, pk):
        products = Product.objects.filter(category=pk)
        print(products)
        serializer = serializers.ProductGetSerializer(products, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = serializers.CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductListCreateAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = serializers.ProductGetSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = serializers.ProductPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        product = get_object_or_404(Product, id=pk)
        return product

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = serializers.ProductGetSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = serializers.ProductPostSerializer(product)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartItemListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=self.request.user.id, )
        serializer = serializers.CartItemGetSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = serializers.CartItemPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItemDetailAPIView(APIView):
    def delete(self, request, pk):
        cart_item = self.get_object(pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=self.request.user.id)
        serializer = serializers.OrderGetSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = serializers.OrderPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cart_item = Cart.objects.filter(user=self.request.user.id)
            cart_item.delete()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailAPIView(APIView):
    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        serializer = serializers.OrderGetSerializer(order)
        return Response(serializer.data)
        