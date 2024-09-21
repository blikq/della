from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    readonly_fields = ("id", "firstname", "lastname")

class ImageInline(admin.TabularInline):  # or use StackedInline for a stacked layout
    model = Image
    extra = 1  # Number of empty forms to display for adding new related objects

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    inlines = [ImageInline]


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)

class BrandAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)

class SizeAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)

class CartItemAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)

class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)

class OrderedItemAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)

class CheckoutDetailsAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)




admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(OrderedItem, OrderedItemAdmin)
admin.site.register(CheckoutDetails, CheckoutDetailsAdmin)


