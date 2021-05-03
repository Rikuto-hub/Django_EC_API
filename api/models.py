from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('email is must')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using= self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

class Profile(models.Model):
    nickName = models.CharField(max_length=20)
    address_num = models.IntegerField()
    address_str = models.CharField(max_length=30, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='userProfile',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nickName


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    
    def total_price():
        total = 0
        for order_product in self.products.all():
            total += order_item.get_total_item_price()
        return total
