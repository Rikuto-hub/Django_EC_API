from django.urls import path, include
from . import views

urlpatterns = [
    path("profile/", views.ProfileListCreateAPIView.as_view(), name="profile"),
    path("category/", views.CategoryListCreateAPIView.as_view(), name="category"),
    path("category/<int:pk>/", views.CategoryDetailAPIView.as_view(), name="category_detail"),
    path("product/", views.ProductListCreateAPIView.as_view(), name="product"),
    path("product/<int:pk>/", views.ProductDetailAPIView.as_view(), name="product_detail"),
    path("cart/", views.CartItemListCreateAPIView.as_view(), name="cart"),
    path("cart/<int:pk>/", views.CartItemDetailAPIView.as_view(), name="cart_detail"),
    path("order/", views.OrderListCreateAPIView.as_view(), name="order"),
    path("order/<int:pk>/", views.OrderDetailAPIView.as_view(), name="order_detail")
]
