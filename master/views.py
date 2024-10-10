from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.db.models import Q
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from .models import *
from eventlog import EventGroup



# Create your views here.
def index_render(request):
    if request.method == "POST":
        if request.POST.get("login-btn") == "LOG IN":
            email = request.POST.get("singin-email")
            password = request.POST.get("singin-password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
            else:
                messages.error(request, "Invalid email or password")
            return redirect(request.META.get('HTTP_REFERER', '/'))

    products = Product.objects.all().order_by('-created_at')[:9]
    products2 = Product.objects.all().order_by('-visited')[:9]
    shoes = Product.objects.filter(category__name="shoes")[:4]

    load = [
        {
            "id": product.id,
            "name": product.name,
            "desc": product.desc,
            "price": str(product.price),
            "created": product.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "ogbrand": product.brand.all(),
            "ogcategory": product.category.all(),
            "ogSize": product.size.all(),
            "ogimages": product.image_set.all(),
        }
        for product in products
    ]

    load2 = [
        {
            "id": product.id,
            "name": product.name,
            "desc": product.desc,
            "price": str(product.price),
            "created": product.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "ogbrand": product.brand.all(),
            "ogcategory": product.category.all(),
            "ogSize": product.size.all(),
            "ogimages": product.image_set.all(),
        }
        for product in products2
    ]

    load_shoes = [
        {
            "id": shoe.id,
            "name": shoe.name,
            "price": str(shoe.price),
            "ogimages": shoe.image_set.all(),
        }
        for shoe in shoes
    ]

    context = {
        "recent": load,
        "popular": load2,
        "shoes": load_shoes,
    }
    return render(request, 'master/index.html', context)


def about_render(request):
    return render(request, 'about.html')








def filter_(request):
    categories = Category.objects.all().order_by('name')
    brands = Brand.objects.all().order_by('name')
    sizes = Size.objects.all().order_by('name')

    list_categories = [{"name": i.name, "id": i.id} for i in categories]
    list_brands = [{"name": i.name, "id": i.id} for i in brands]
    list_sizes = [{"name": i.name, "id": i.id} for i in sizes]

    if request.method == "POST":
        filter_category = request.POST.getlist('category')
        filter_brand = request.POST.getlist('brand')
        filter_size = request.POST.getlist('size')

        filter_kwargs = {}
        if filter_category:
            filter_kwargs['category__id__in'] = filter_category
        if filter_brand:
            filter_kwargs['brand__id__in'] = filter_brand
        if filter_size:
            filter_kwargs['size__id__in'] = filter_size

        filtered_products = Product.objects.filter(**filter_kwargs).distinct()
        
        load = [
            {
                "id": product.id,
                "name": product.name,
                "desc": product.desc,
                "price": str(product.price),
                "created": product.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "ogbrand": product.brand.all(),
                "ogcategory": product.category.all(),
                "ogSize": product.size.all(),
                "ogimages": product.image_set.all(),
            }
            for product in filtered_products
        ]

        paginator = Paginator(load, 9)
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {'page_obj': page_obj, 'categories': list_categories, 'sizes': list_sizes, 'brands': list_brands}
        return context

    return {'categories': list_categories, 'sizes': list_sizes, 'brands': list_brands}

def all_products_render(request):
    if request.method == "POST":
        return render(request, 'master/all-products.html', context=filter_(request))

    products = Product.objects.all().order_by('-created_at')
    load = [
        {
            "id": product.id,
            "name": product.name,
            "desc": product.desc,
            "price": str(product.price),
            "created": product.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "ogbrand": product.brand.all(),
            "ogcategory": product.category.all(),
            "ogSize": product.size.all(),
            "ogimages": product.image_set.all(),
        }
        for product in products
    ]

    paginator = Paginator(load, 9)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {**filter_(request), 'page_obj': page_obj}
    return render(request, 'master/all-products.html', context)

def product_render(request, id):
    try:
        product = get_object_or_404(Product, id=id)
    except Http404:
        messages.error(request, "Product not found")
        return redirect('/all-products')

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("/login")

        if request.POST.get("Submit") == "Add to cart":
            size = request.POST.get("size")
            quantity = request.POST.get("quantity")
            try:
                size_obj = Size.objects.get(name=size)
                cart_item = CartItem.objects.create(user=request.user, product=product, size=size_obj, quantity=int(quantity))
                messages.success(request, "Item added to cart successfully")
            except ObjectDoesNotExist:
                messages.error(request, "Invalid size selected")
            except ValueError:
                messages.error(request, "Invalid quantity")
            return redirect(request.path_info)

        if request.POST.get("submit-review") == "Submit Review":
            stars = min(int(request.POST.get("rating", 1)), 5)
            msg = ["Poor", "Fair", "Good", "Very Good", "Excellent"][stars-1]
            review = request.POST.get("review")
            Review.objects.create(user=request.user, product=product, stars=stars, review=review, msg=msg)
            messages.success(request, "Review submitted successfully")
            return redirect(request.path_info)

    product.visited += 1
    product.save()

    popular_products = Product.objects.all().order_by('-visited')[:9]
    load2 = [
        {
            "id": p.id,
            "name": p.name,
            "desc": p.desc,
            "price": str(p.price),
            "created": p.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "ogbrand": p.brand.all(),
            "ogcategory": p.category.all(),
            "ogSize": p.size.all(),
            "ogimages": p.image_set.all(),
        }
        for p in popular_products
    ]

    reviews = Review.objects.filter(product=product).order_by('-created_at')
    for review in reviews:
        review.created_at = review.created_at.date()
        review.stars *= 20

    context = {
        "product": {
            "id": product.id,
            "name": product.name,
            "desc": product.desc,
            "price": str(product.price),
            "created": product.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "ogbrand": product.brand.all(),
            "ogcategory": product.category.all(),
            "ogsize": product.size.all(),
            "ogimages": product.image_set.all(),
        },
        "reviews": reviews,
        "popular": load2
    }
    
    return render(request, 'master/product.html', context)

def category_render(request, name):
    try:

        category_obj = Category.objects.get(name=name)

    except Category.DoesNotExist:
        messages.error(request, f"Category '{name}' does not exist")
        return redirect('/all-products')

    products = Product.objects.filter(category=category_obj)
    load = [
        {
            "id": product.id,
            "name": product.name,
            "desc": product.desc,
            "price": str(product.price),
            "created": product.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "ogbrand": product.brand.all(),
            "ogcategory": product.category.all(),
            "ogSize": product.size.all(),
            "ogimages": product.image_set.all(),
        }
        for product in products
    ]

    paginator = Paginator(load, 9)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {'page_obj': page_obj, 'categoryname': name}
    return render(request, 'master/category.html', context)

@login_required(login_url="/login")
def cart_render(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user).select_related('product')
    
    load = [
        {
            "cart_item": cart_item,
            "total": cart_item.product.price * cart_item.quantity,
            "images": cart_item.product.image_set.all()
        }
        for cart_item in cart_items
    ]

    subtotal = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)

    delete_item = request.GET.get("delete-item")
    if delete_item:
        try:
            cart_item = CartItem.objects.get(id=delete_item, user=user)
            cart_item.delete()
            messages.success(request, "Item removed from cart")
        except CartItem.DoesNotExist:
            messages.error(request, "Item not found in cart")
        return redirect("/cart")

    if request.method == "POST" and request.POST.get("Update Cart") == "Update Cart":
        for cart_item in cart_items:
            quantity = request.POST.get(f"quantity-item-{cart_item.id}")
            if quantity:
                try:
                    cart_item.quantity = int(quantity)
                    cart_item.save()
                except ValueError:
                    messages.error(request, f"Invalid quantity for {cart_item.product.name}")
        messages.success(request, "Cart updated successfully")
        return redirect("/cart")

    return render(request, 'master/cart.html', {'cart_items': load, 'subtotal': subtotal})

@login_required(login_url="/login")
def dashboard_render(request):
    orders = OrderedItem.objects.filter(user=request.user).select_related('cart_item__product')
    load = [
        {
            "order": order,
            "images": order.cart_item.product.image_set.all()
        }
        for order in orders
    ]
    
    try:
        c_details = CheckoutDetails.objects.get(user=request.user)
    except CheckoutDetails.DoesNotExist:
        c_details = None

    context = {
        "orders": load,
        "c_details": c_details
    }
    return render(request, 'master/dashboard.html', context=context)

def shop_render(request):
    return render(request, 'master/shop.html')



def contact_render(request):
    return render(request, 'master/contact.html')

def faq_render(request):
    return render(request, 'master/faq.html')

@login_required(login_url="/login", redirect_field_name="next")
def wishlist_render(request):
    user = request.user
    wishlist = Wishlist.objects.filter(user=user).select_related('product')
    load = [
        {
            "product": item.product,
            "images": item.product.image_set.all(),
            "stock": item.product.stock > 0
        }
        for item in wishlist
    ]
    context = {
        "wishlist_items": load
    }
    return render(request, 'master/wishlist.html', context)

@login_required(login_url="/login")
def add_to_wishlist_render(request, id):
    user = request.user
    try:
        product = Product.objects.get(id=id)
        wishlist, created = Wishlist.objects.get_or_create(user=user, product=product)
        if created:
            messages.success(request, "Product added to wishlist")
        else:
            messages.info(request, "Product already in wishlist")
    except Product.DoesNotExist:
        messages.error(request, "Product not found")
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url="/login")
def remove_from_wishlist_render(request, id):
    user = request.user
    try:
        product = Product.objects.get(id=id)
        wishlist = Wishlist.objects.filter(user=user, product=product)
        if wishlist.exists():
            wishlist.delete()
            messages.success(request, "Product removed from wishlist")
        else:
            messages.info(request, "Product not in wishlist")
    except Product.DoesNotExist:
        messages.error(request, "Product not found")
    return redirect(request.META.get('HTTP_REFERER', '/'))

def logout_render(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect(request.META.get('HTTP_REFERER', '/'))

def search(context):
    return Product.objects.filter(Q(name__icontains=context) | Q(desc__icontains=context))

def search_render(request):
    context = request.GET.get("s", "")
    products = search(context)
    load = [
        {
            "id": product.id,
            "name": product.name,
            "desc": product.desc,
            "price": str(product.price),
            "created": product.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "ogbrand": product.brand.all(),
            "ogcategory": product.category.all(),
            "ogSize": product.size.all(),
            "ogimages": product.image_set.all(),
        }
        for product in products
    ]

    paginator = Paginator(load, 9)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {'page_obj': page_obj, 'search': context}
    return render(request, 'master/search.html', context=context)

@login_required(login_url="/login")
def add_to_cart_render(request, id):
    try:
        product = Product.objects.get(id=id)
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            size=product.size.first(),
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        messages.success(request, "Product added to cart")
    except Product.DoesNotExist:
        messages.error(request, "Product not found")
    return redirect(request.META.get('HTTP_REFERER', '/'))

def register_render(request):
    if request.method == "POST" and request.POST.get("register-btn") == "Sign Up":
        email = request.POST.get("register-email")
        password = request.POST.get("register-password")
        firstname = request.POST.get("register-firstname")
        lastname = request.POST.get("register-lastname")
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
        else:
            user = CustomUser.objects.create_user(email=email, password=password, firstname=firstname, lastname=lastname)
            user.is_active = False
            user.save()
            login(request, user)
            messages.success(request, "Account created successfully. Please verify your email.")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'accounts/register.html')

def login_render(request):
    if request.method == "POST":
        email = request.POST.get("singin-email")
        password = request.POST.get("singin-password")
        print(request.POST.get("singin-email"))
        print(request.POST.get("singin-password"))
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
        else:
            messages.error(request, "Invalid email or password")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'accounts/login.html')

#######################payment
@login_required(login_url="/login")
def checkout_render(request):
    user = request.user
    try:
        c_d = CheckoutDetails.objects.get(user=user)
    except CheckoutDetails.DoesNotExist:
        c_d = None

    if request.method == "POST" and request.POST.get("submit-details") == "Save Details":
        checkout_details, created = CheckoutDetails.objects.update_or_create(
            user=user,
            defaults={
                'firstname': request.POST.get("firstname"),
                'lastname': request.POST.get("lastname"),
                'company': request.POST.get("company"),
                'country': request.POST.get("country"),
                'address': request.POST.get("address"),
                'building': request.POST.get("building"),
                'city': request.POST.get("city"),
                'state': request.POST.get("state"),
                'zip_code': request.POST.get("zip-code"),
                'phone': request.POST.get("phone"),
                'notes': request.POST.get("notes"),
                'email': request.POST.get("email")
            }
        )
        messages.success(request, "Checkout details saved successfully")
        return redirect("/checkout")




    cart_items = CartItem.objects.filter(user=user).select_related('product')
    subtotal = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)

    if request.method == "POST" and request.POST.get("placeorder") == "Place Order":
        checkout_details, created = CheckoutDetails.objects.update_or_create(
            user=user,
            defaults={
                'firstname': request.POST.get("firstname"),
                'lastname': request.POST.get("lastname"),
                'company': request.POST.get("company"),
                'country': request.POST.get("country"),
                'address': request.POST.get("address"),
                'building': request.POST.get("building"),
                'city': request.POST.get("city"),
                'state': request.POST.get("state"),
                'zip_code': request.POST.get("zip-code"),
                'phone': request.POST.get("phone"),
                'notes': request.POST.get("notes"),
                'email': request.POST.get("email")
            }
        )
        p = Payment.objects.create(amount=subtotal, user=user)
        p.save()
        for i in cart_items:
            
            s = SessionPaymentItems.objects.create(payment=p, cart_item=i, user=request.user)
            s.save()
        return redirect(f"/initiate-payment?ref={p.ref}")

    context = {
        "checkout_details": c_d,
        "cart_items": cart_items,
        "subtotal": subtotal
    }

    return render(request, 'master/checkout.html', context)



@login_required(login_url="/login")
def initiate_payment(request):
    e = EventGroup()
    try:
        e.info(f"{request.user.email} Creating userwallet if not existing")
        UserWallet.objects.create(user=request.user).save()
    except:
        e.info(f"{request.user.email} Userwallet already exists")
        pass

    ref = request.GET.get("ref")
    payment = Payment.objects.get(ref=ref)


    e.info(f"{request.user.email} Creating payment page")


    pk = settings.PAYSTACK_PUBLIC_KEY

    context = {
        'payment': payment,
        'field_values': request.POST,
        'paystack_pub_key': pk,
        'amount_value': payment.amount_value(),
    }
    return render(request, 'master/make_payment.html', context)



@login_required(login_url="/login")
def verify_payment(request, ref):
    e = EventGroup()
    payment = Payment.objects.get(ref=ref)
    verified = payment.verify_payment()


    if verified:
        e.info(f"{request.user.email} Payment verified successfully")
        for i in SessionPaymentItems.objects.filter(payment=payment):
            OrderedItem.objects.create(user=request.user, product=i.cart_item.product, size=i.cart_item.size, quauntity=i.cart_item.quantity).save()
            c = CartItem.objects.get(id=i.cart_item.id)
            c.delete()
            i.delete()


        try:
            e.info(f"{request.user.email} Funding wallet")
            user_wallet = UserWallet.objects.get(user=request.user)
            user_wallet.balance += payment.amount
            user_wallet.save()
            e.info(f"{request.user.email} payment processed successfully")
            print(request.user.username, " payment processed successfully")
        except:
            e.error(f"{request.user.email} Failed to process payment")
            print(request.user.username, " failed to process payment")
        return render(request, "master/success.html", {"ref": ref})
    return render(request, "master/index.html")

