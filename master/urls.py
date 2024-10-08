from django.urls import path
from .views import *

urlpatterns = [
    path('', index_render, name="home"),
    path('shop', shop_render, name="shop"),
    path('category/<str:name>', category_render, name="category"),
    path('all-products', all_products_render, name="all-products"),

    path('cart', cart_render, name="cart"),
    path('checkout', checkout_render, name="checkout"),
    path('contact', contact_render, name="contact"),

    path('about', about_render, name="about-us"),
    path('faq', faq_render, name="faq"),
    path('dashboard', dashboard_render, name="dashboard"),
    path('product/<int:id>', product_render, name="product"),
    path('wishlist', wishlist_render, name="wishlist"),
    path('logout', logout_render, name="logout"),
    path('login', login_render, name="login"),
    path('search', search_render, name="search"),
    path('add-to-wishlist/<int:id>', add_to_wishlist_render, name="add-to-wishlist"),
    path('remove-from-wishlist/<int:id>', remove_from_wishlist_render, name="remove-from-wishlist"),
    path('add-to-cart/<int:id>', add_to_cart_render, name="add-to-cart"),
    path('login', login_render, name="login"),
    path('register', register_render, name="register"),
    path('initiate-payment', initiate_payment, name="initiate-payment"),
    path('verify-payment/<str:ref>', verify_payment, name="verify-payment"),
]

#ignore for media routing   
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)