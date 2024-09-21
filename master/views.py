

from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


from .models import *



# Create your views here.
def index_render(request):

    if request.method == "POST":
        if request.POST.get("login-btn") == "LOG IN":
            email = request.POST.get("singin-email")
            password = request.POST.get("singin-password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)

            return redirect(request.META.get('HTTP_REFERER', '/'))




    products = Product.objects.all().reverse()[:9]
    # products[0].brand.
    load = []
    
    for product in products:
        images = Image.objects.filter(product_id=product.id)
        load.append(
            {
                "id": product.id,
                "name": product.name,
                "desc": product.desc,
                "price": str(product.price),
                "created": f"{product.created_at.replace(microsecond=0).date()} {product.created_at.replace(microsecond=0).time()}",
                "ogbrand": product.brand.all(),
                "ogcategory": product.category.all(),
                "ogSize": product.size.all(),
                "ogimages": images,
            }
        )

    products2 = Product.objects.all().order_by('-visited')[:9]
    # products[0].brand.
    load2 = []
    
    for product in products2:
        images = Image.objects.filter(product_id=product.id)
        load2.append(
            {
                "id": product.id,
                "name": product.name,
                "desc": product.desc,
                "price": str(product.price),
                "created": f"{product.created_at.replace(microsecond=0).date()} {product.created_at.replace(microsecond=0).time()}",
                "ogbrand": product.brand.all(),
                "ogcategory": product.category.all(),
                "ogSize": product.size.all(),
                "ogimages": images,
            }
        )

    shoes = Product.objects.filter(category__name="shoes")[:4]
    load_shoes = []
    for shoe in shoes:
        images = Image.objects.filter(product_id=shoe.id)
        load_shoes.append(
            {
                "id": shoe.id,
                "name": shoe.name,
                "price": str(shoe.price),
                "ogimages": images,


            }
        )


    context = {
        "recent": load,
        "popular": load2,
        "shoes": load_shoes,
    }
    return render(request, 'master/index.html', context)


def filter_(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    sizes = Size.objects.all()

    list_categories = []
    for i in categories:
        list_categories.append({"name": i.name, "id": i.id})
    # Sort list_categories alphabetically
    list_categories.sort(key=lambda x: x['name'])

    list_brands = []
    for i in brands:
        list_brands.append({"name": i.name, "id": i.id})
    # Sort list_brands alphabetically
    list_brands.sort(key=lambda x: x['name'])

    
    list_sizes = []
    for i in sizes:
        list_sizes.append({"name": i.name, "id": i.id})
    # Sort list_sizes alphabetically
    list_sizes.sort(key=lambda x: x['name'])

    if request.method == "POST":
        filter_category = request.POST.getlist('category')
        filter_brand = request.POST.getlist('brand')
        filter_size = request.POST.getlist('size')

        try:
            # Convert filter_category to a list of integers
            filter_category_int = [int(category_id) for category_id in filter_category if category_id.isdigit()]
            cat_list = [Category.objects.get(id=i_cate) for i_cate in filter_category_int]

            filter_brand_int = [int(brand_id) for brand_id in filter_brand if brand_id.isdigit()]
            brand_list = [Brand.objects.get(id=i_brand) for i_brand in filter_brand_int]

            filter_size_int = [int(size_id) for size_id in filter_size if size_id.isdigit()]
            size_list = [Size.objects.get(id=i_size) for i_size in filter_size_int if isinstance(i_size, int)]
        except:
            pass
        
        filter_kwargs = {}
        if cat_list:
            filter_kwargs['category__in'] = cat_list
        if brand_list:
            filter_kwargs['brand__in'] = brand_list
        if size_list:
            filter_kwargs['size__in'] = size_list
        filtered_products = Product.objects.filter(**filter_kwargs).distinct()
        load = []

        for product in filtered_products:
            images = Image.objects.filter(product_id=product.id)
            load.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "desc": product.desc,
                    "price": str(product.price),
                    "created": f"{product.created_at.replace(microsecond=0).date()} {product.created_at.replace(microsecond=0).time()}",
                    "ogbrand": product.brand.all(),
                    "ogcategory": product.category.all(),
                    "ogSize": product.size.all(),
                    "ogimages": images,
                }
            )

        p = Paginator(load, 9)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = p.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = p.page(p.num_pages)
        context = {'page_obj': page_obj, 'categories': list_categories, 'sizes': list_sizes, 'brands': list_brands}

        return context


def all_products_render(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    sizes = Size.objects.all()

    list_categories = []
    for i in categories:
        list_categories.append({"name": i.name, "id": i.id})
    # Sort list_categories alphabetically
    list_categories.sort(key=lambda x: x['name'])

    list_brands = []
    for i in brands:
        list_brands.append({"name": i.name, "id": i.id})
    # Sort list_brands alphabetically
    list_brands.sort(key=lambda x: x['name'])

    
    list_sizes = []
    for i in sizes:
        list_sizes.append({"name": i.name, "id": i.id})
    # Sort list_sizes alphabetically
    list_sizes.sort(key=lambda x: x['name'])
    
    if request.method == "POST":
        return render(request, 'master/all-products.html', context=filter_(request))


    #page logic
    products = Product.objects.all().reverse()
    load = []


    for product in products:
        images = Image.objects.filter(product_id=product.id)
        load.append(
            {
                "id": product.id,
                "name": product.name,
                "desc": product.desc,
                "price": str(product.price),
                "created": f"{product.created_at.replace(microsecond=0).date()} {product.created_at.replace(microsecond=0).time()}",
                "ogbrand": product.brand.all(),
                "ogcategory": product.category.all(),
                "ogSize": product.size.all(),
                "ogimages": images,
            }
        )

    p = Paginator(load, 9)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj, 'categories': list_categories, 'sizes': list_sizes, 'brands': list_brands}

    return render(request, 'master/all-products.html', context)


def product_render(request, id):

    if request.method == "POST":
        if request.user.is_authenticated:
            if request.POST.get("Submit") == "Add to cart":
                user = request.user
                size = request.POST.get("size")
                quantity = request.POST.get("quantity")
                size_obj = Size.objects.get(name=size)
                product = Product.objects.get(id=int(id))
                cart_item = CartItem.objects.create(user=user, product=product, size=size_obj, quantity=int(quantity))
                cart_item.save()

                return redirect(request.path_info)
        else:
            return redirect("/login")


    if request.method == "POST":
        if request.user.is_authenticated:
            if request.POST.get("submit-review") == "Submit Review":
                user = request.user
                product = Product.objects.get(id=id)
                stars = request.POST.get("rating")
                msg = ""
                if int(stars) <= 1:
                    msg = "Poor"
                elif int(stars) == 2:
                    msg = "Fair"
                elif int(stars) == 3:
                    msg = "Good"
                elif int(stars) == 4:
                    msg = "Very Good"
                elif int(stars) >= 5:
                    msg = "Excellent"
                review = request.POST.get("review")
                if int(stars) > 5:
                    stars = 5
                review_obj = Review.objects.create(user=user, product=product, stars=int(stars), review=review, msg=msg)
                review_obj.save()
                return redirect(request.path_info)

    products2 = Product.objects.all().order_by('-visited')[:9]
    # products[0].brand.
    load2 = []
    
    for product in products2:
        images = Image.objects.filter(product_id=product.id)
        load2.append(
            {
                "id": product.id,
                "name": product.name,
                "desc": product.desc,
                "price": str(product.price),
                "created": f"{product.created_at.replace(microsecond=0).date()} {product.created_at.replace(microsecond=0).time()}",
                "ogbrand": product.brand.all(),
                "ogcategory": product.category.all(),
                "ogSize": product.size.all(),
                "ogimages": images,
            }
        )


    product = Product.objects.get(id=id)
    product.visited += 1
    product.save()

    images = Image.objects.filter(product=product)
    reviews = Review.objects.filter(product=product).reverse()
    for i in reviews:
        i.created_at = i.created_at.replace(microsecond=0).date()
        i.stars *= 20
    product = {
                "id": product.id,
                "name": product.name,
                "desc": product.desc,
                "price": str(product.price),
                "created": f"{product.created_at.replace(microsecond=0).date()} {product.created_at.replace(microsecond=0).time()}",
                "ogbrand": product.brand.all(),
                "ogcategory": product.category.all(),
                "ogsize": product.size.all(),
                "ogimages": images,
    }
    context = {
        "product": product,
        "reviews": reviews,
        "popular": load2

    }
    
    return render(request, 'master/product.html', context)

def category_render(request, name):

    load = []
    try:
        category_obj = Category.objects.get(name=name)
        products = Product.objects.filter(category=category_obj)
        for product in products:
            images = Image.objects.filter(product_id=product.id)
            load.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "desc": product.desc,
                    "price": str(product.price),
                    "created": product.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "ogbrand": product.brand.all(),
                    "ogcategory": product.category.all(),
                    "ogSize": product.size.all(),
                    "ogimages": images,
                
                }
            )
    except:
        pass

    p = Paginator(load, 9)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj, 'categoryname': name}

    return render(request, 'master/category.html', context)


@login_required(login_url="/login")
def cart_render(request):
    user = request.user
    load = []
    cart_items = CartItem.objects.filter(user=user)
    subtotal = 0
    for cart_item in cart_items:
        subtotal += cart_item.product.price * cart_item.quantity
        load.append({"cart_item": cart_item, "images": Image.objects.filter(product_id=cart_item.product.id)})

    delete_item = request.GET.get("delete-item")
    if delete_item:
        cart_item = CartItem.objects.get(id=delete_item)
        cart_item.delete()
        return redirect("cart")

    if request.method == "POST":
        if request.POST.get("Update Cart") == "Update Cart":
            for cart_item in cart_items:
                cart_item.quantity = int(request.POST.get(f"quantity-item-{cart_item.id}"))
                cart_item.save()
                return redirect("cart")

    return render(request, 'master/cart.html', {'cart_items': load, 'subtotal': subtotal})


def login_render(request):
    if request.method == "POST":
        if request.POST.get("login-btn") == "LOG IN":
            email = request.POST.get("singin-email")
            password = request.POST.get("singin-password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)

            return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url="/login")
def dashboard_render(request):
    load = []
    orders = OrderedItem.objects.filter(user = request.user)
    for order in orders:
        load.append({"order": order, "images": Image.objects.filter(product_id=order.cart_item.product.id)})
    c_details = CheckoutDetails.objects.get(user = request.user)
    

    context = {
        "orders": load,
        "c_details": c_details
    }
    return render(request, 'master/dashboard.html', context = context)

def shop_render(request):
    return render(request, 'master/shop.html')


@login_required(login_url="/login")
def checkout_render(request):

    user = request.user
    firstname = request.POST.get("firstname")
    lastname = request.POST.get("lastname")
    company = request.POST.get("company")
    country = request.POST.get("country")
    address = request.POST.get("address")
    building = request.POST.get("building")
    city = request.POST.get("city")
    state = request.POST.get("state")
    zip_code = request.POST.get("zip-code")
    phone = request.POST.get("phone")
    notes = request.POST.get("notes")
    c_d = CheckoutDetails.objects.get(user=user)
    if request.method == "POST":
        if request.POST.get("submit-details") == "Save Details":
            
            checkout_details, created = CheckoutDetails.objects.update_or_create(
                user=user,
                defaults={
                    'firstname': firstname,
                    'lastname': lastname,
                    'company': company,
                    'country': country,
                    'address': address,
                    'building': building,
                    'city': city,
                    'state': state,
                    'zip_code': zip_code,
                    'phone': phone,
                    'notes': notes
                }
            )
            checkout_details.save()
    context = {
        "checkout_details": c_d
    }
    return render(request, 'master/checkout.html', context)

def contact_render(request):
    return render(request, 'master/contact.html')

def faq_render(request):
    return render(request, 'master/faq.html')


@login_required(login_url="#signin-modal", redirect_field_name="next")
def wishlist_render(request):
    user = request.user
    wishlist = Wishlist.objects.filter(user=user)
    load = []
    
    for item in wishlist:
        product = Product.objects.get(id=item.product.id)
        images = Image.objects.filter(product_id=product.id)
        stock = False
        if product.stock > 0:
            stock = True
        else:
            stock = False
        load.append({"product": product, "images": images, "stock": stock})
    context = {
        "wishlist_items": load
    }
    return render(request, 'master/wishlist.html', context)

@login_required(login_url="/login")
def add_to_wishlist_render(request, id):
    user = request.user
    product = Product.objects.get(id=id)
    wishlist = Wishlist.objects.create(user=user, product=product)
    wishlist.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url="/login")
def remove_from_wishlist_render(request, id):
    user = request.user
    product = Product.objects.get(id=id)
    wishlist = Wishlist.objects.filter(user=user, product=product)
    wishlist.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def logout_render(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def search(context):
    result = Product.objects.filter(name__icontains=context)
    return result

def search_render(request):
    context = request.GET.get("s")
    products = search(context)
    load = []
    for product in products:
        images = Image.objects.filter(product_id=product.id)
        load.append(
            {
                "id": product.id,
                "name": product.name,
                "desc": product.desc,
                "price": str(product.price),
                "created": product.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "ogbrand": product.brand.all(),
                "ogcategory": product.category.all(),
                "ogSize": product.size.all(),
                "ogimages": images,
            
            }
        )

    p = Paginator(load, 9)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj, 'search': context}


    return render(request, 'master/search.html', context=context)

def add_to_cart_render(request, id):
    user = request.user
    product = Product.objects.get(id=id)
    cart_item = CartItem.objects.create(user=user, product=product, size=product.size.all()[0], quantity=1)
    cart_item.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


def register_render(request):
    if request.method == "POST":
        if request.POST.get("register-btn") == "Sign Up":
            email = request.POST.get("register-email")
            password = request.POST.get("register-password")
            firstname = request.POST.get("register-firstname")
            lastname = request.POST.get("register-lastname")
            user = CustomUser.objects.create(email=email, password=password, firstname=firstname, lastname=lastname)
            user.is_active = False
            user.save()
            login(request, user)
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'master/register.html')



def login_render(request):
    if request.method == "POST":
        if request.POST.get("login-btn") == "LOG IN":
            email = request.POST.get("singin-email")
            password = request.POST.get("singin-password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)

            return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'master/login.html')