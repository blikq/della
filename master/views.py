

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

    context = {
        "recent": load
    }
    return render(request, 'master/index.html', context)

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

        return render(request, 'master/filter-category.html', context)


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
    user = CustomUser.objects.get(email="a@a.com")

    if request.method == "POST":
        if request.user.is_authenticated:
            if request.POST.get("Submit") == "Add to cart":
                size = request.POST.get("size")
                quantity = request.POST.get("quantity")
                size_obj = Size.objects.get(name=size)
                product = Product.objects.get(id=int(id))
                cart_item = CartItem.objects.create(user=user, product=product, size=size_obj, quantity=int(quantity))
                cart_item.save()

                return redirect("cart")
        else:
            return redirect("/#signin-modal")

    product = Product.objects.get(id=id)
    images = Image.objects.filter(product_id=product.id)
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

    }
    
    return render(request, 'master/product.html', context)

def category_render(request, name):
    category_obj = Category.objects.get(name=name)
    products = Product.objects.filter(category=category_obj)
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
    context = {'page_obj': page_obj, 'categoryname': name}

    return render(request, 'master/category.html', context)


@login_required(login_url="/#signin-modal")
def cart_render(request):
    user = request.user

    cart_items = CartItem.objects.filter(user=user)
    subtotal = 0
    for cart_item in cart_items:
        subtotal += cart_item.product.price * cart_item.quantity

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

    return render(request, 'master/cart.html', {'cart_items': cart_items, 'subtotal': subtotal})

def shop_render(request):
    return render(request, 'master/shop.html')



def checkout_render(request):
    return render(request, 'master/checkout.html')

def contact_render(request):
    return render(request, 'master/contact.html')

def faq_render(request):
    return render(request, 'master/faq.html')

def dashboard_render(request):
    return render(request, 'master/dashboard.html')


def wishlist_render(request):
    return render(request, 'master/wishlist.html')

def logout_render(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

