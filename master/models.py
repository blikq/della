from django.db import models


from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager





# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

class Brand(models.Model):
    name = models.CharField(max_length=200, unique=True)


    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

class Size(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=1024)
    visited = models.IntegerField(default=0)

    price = models.IntegerField()
    category = models.ManyToManyField(Category)
    brand = models.ManyToManyField(Brand)
    size = models.ManyToManyField(Size)
    stock = models.IntegerField()

    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)



class Image(models.Model):
    images = models.ImageField(upload_to="upimages/")

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        blank=False
    )

    def __str__(self):
        return str(self.images)







class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    firstname = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100, blank=True)

    # cart = models.ManyToManyField(Product, blank=True)


    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    # REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    

    def __str__(self):
        return f"{self.user.email} - {self.product.name} - {self.size.name} - {self.quantity}"

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    msg = models.CharField(max_length=50)
    review = models.CharField(max_length=250)
    stars = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.product.name} - {self.msg} - {self.review} - {self.stars}"



class OrderedItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    cart_item = models.ForeignKey(CartItem, on_delete=models.PROTECT)
    delivered = models.BooleanField(default=False)

    delivered_at = models.DateTimeField(default=None, null=True)

class CheckoutDetails(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    building = models.CharField(max_length=200)

    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    notes = models.CharField(max_length=200)
    
class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"