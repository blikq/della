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
    path('faq', faq_render, name="faq"),
    path('dashboard', dashboard_render, name="dashboard"),
    path('product/<int:id>', product_render, name="product"),
    path('wishlist', wishlist_render, name="wishlist"),
    path('logout', logout_render, name="logout"),
]

#ignore for media routing   
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)