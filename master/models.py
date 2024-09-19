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

    price = models.IntegerField()
    category = models.ManyToManyField(Category)
    brand = models.ManyToManyField(Brand)
    size = models.ManyToManyField(Size)
    stock = models.IntegerField()

    created_at = models.DateTimeField()

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

    email = models.EmailField(unique=True   )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

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
        return f"{self.user.username} - {self.product.name} - {self.size.name} - {self.quantity}"