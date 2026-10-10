
from decimal import Decimal
from django.conf import settings

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login
from django.http import JsonResponse
from django.db.models import Q

from .models import Category, SubCategory, Product

from django.contrib import messages
from .models import ContactMessage

# =========================================================
# HOME
# =========================================================

def home(request):
    categories = Category.objects.all()

    products = Product.objects.filter(
        available=True
    ).select_related(
        'category',
        'subcategory'
    ).order_by('-created_at')

    return render(
        request,
        'home.html',
        {
            'categories': categories,
            'products': products,
            'USE_STATIC_MEDIA': settings.USE_STATIC_MEDIA,
        }
    )


# =========================================================
# PRODUCT DETAIL
# =========================================================

def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    # Related products
    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(
        id=product.id
    ).order_by('-created_at')[:4]

    # Discount percentage
    discount_percent = None

    if product.old_price and product.old_price > product.price:

        discount_percent = round(
            (
                (product.old_price - product.price)
                / product.old_price
            ) * 100
        )

    return render(
        request,
        'product_detail.html',
        {
            'product': product,
            'related_products': related_products,
            'discount_percent': discount_percent,
        }
    )


# =========================================================
# ADD TO CART
# =========================================================

def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    # Existing quantity + 1
    cart[product_id] = cart.get(product_id, 0) + 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')












# =========================================================
# BUY NOW
# =========================================================

def buy_now(request, item_type, item_id):

    # Sab categories Product model se aa rahi hain
    product = get_object_or_404(
        Product,
        id=item_id,
        available=True
    )

    # Temporary buy-now cart
    buy_now_cart = {
        str(product.id): 1
    }

    # Existing cart ko disturb nahi karega
    request.session['buy_now_cart'] = buy_now_cart
    request.session.modified = True

    return redirect('checkout')
























# =========================================================
# CART
# =========================================================

def cart(request):

    cart_data = request.session.get('cart', {})

    cart_items = []
    total = Decimal('0.00')

    for item_key, quantity in cart_data.items():

        # -------------------------------------------------
        # Old cart format protection
        # -------------------------------------------------

        if isinstance(quantity, dict):
            quantity = quantity.get('quantity', 1)

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            quantity = 1

        if quantity < 1:
            quantity = 1

        # -------------------------------------------------
        # ALL PRODUCTS
        # -------------------------------------------------

        try:

            product = Product.objects.select_related(
                'category',
                'subcategory'
            ).get(
                id=int(item_key),
                available=True
            )

        except (
            Product.DoesNotExist,
            ValueError,
            TypeError
        ):
            continue

        # -------------------------------------------------
        # SUBTOTAL
        # -------------------------------------------------

        subtotal = product.price * quantity

        total += subtotal

        # -------------------------------------------------
        # CART ITEM
        # -------------------------------------------------

        cart_items.append({
            'item_key': item_key,
            'item_type': 'product',
            'product': product,
            'quantity': quantity,
            'price': product.price,
            'subtotal': subtotal,
        })

    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(
        request,
        'cart.html',
        context
    )


# =========================================================
# REMOVE FROM CART
# =========================================================

def remove_from_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


# =========================================================
# DECREASE CART QUANTITY
# =========================================================

def decrease_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:

        quantity = cart[product_id]

        # Old dictionary format protection
        if isinstance(quantity, dict):
            quantity = quantity.get('quantity', 1)

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            quantity = 1

        if quantity > 1:

            cart[product_id] = quantity - 1

        else:

            del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


# =========================================================
# INCREASE CART QUANTITY
# =========================================================

def increase_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:

        quantity = cart[product_id]

        # Old dictionary format protection
        if isinstance(quantity, dict):
            quantity = quantity.get('quantity', 1)

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            quantity = 1

        cart[product_id] = quantity + 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Password check
        if password != confirm_password:

            return render(
                request,
                "register.html",
                {
                    "error": "Passwords do not match."
                }
            )

        # Username check
        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                "register.html",
                {
                    "error": "Username already exists."
                }
            )

        # Email check
        if User.objects.filter(
            email=email
        ).exists():

            return render(
                request,
                "register.html",
                {
                    "error": "Email already exists."
                }
            )

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Login
        login(
            request,
            user
        )

        return redirect("home")

    return render(
        request,
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            auth_login(
                request,
                user
            )

            return redirect("home")

        else:

            return render(
                request,
                "login.html",
                {
                    "error": "Invalid username or password."
                }
            )

    return render(
        request,
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    auth_logout(request)

    return redirect("home")


# =========================================================
# CATEGORIES PAGE
# =========================================================

def categories_view(request):

    categories = Category.objects.all().order_by('name')

    context = {
        'categories': categories,
    }

    return render(
        request,
        'categories.html',
        context
    )


# =========================================================
# CATEGORY PRODUCTS
# =========================================================

def category_products(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id
    )

    # Only selected category products
    products = Product.objects.filter(
        category_id=category_id,
        available=True
    ).select_related(
        'category',
        'subcategory'
    ).order_by('-created_at')

    context = {
        'category': category,
        'products': products,
    }

    return render(
        request,
        'category_products.html',
        context
    )


# =========================================================
# CHECKOUT
# =========================================================

def checkout(request):

    cart_data = request.session.get('cart', {})

    cart_items = []
    total = Decimal('0.00')

    # =====================================================
    # CART ITEMS
    # =====================================================

    for item_key, quantity in cart_data.items():

        # -------------------------------------------------
        # Old cart format protection
        # -------------------------------------------------

        if isinstance(quantity, dict):
            quantity = quantity.get('quantity', 1)

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            quantity = 1

        if quantity < 1:
            quantity = 1

        # -------------------------------------------------
        # PRODUCT
        # -------------------------------------------------

        try:

            product = Product.objects.select_related(
                'category',
                'subcategory'
            ).get(
                id=int(item_key),
                available=True
            )

        except (
            Product.DoesNotExist,
            ValueError,
            TypeError
        ):
            continue

        # -------------------------------------------------
        # SUBTOTAL
        # -------------------------------------------------

        subtotal = product.price * quantity

        total += subtotal

        cart_items.append({
            'item_key': item_key,
            'item_type': 'product',
            'product': product,
            'quantity': quantity,
            'price': product.price,
            'subtotal': subtotal,
        })

    # =====================================================
    # PLACE ORDER
    # =====================================================

    if request.method == 'POST':

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        payment = request.POST.get('payment')

        # -------------------------------------------------
        # EMPTY CART CHECK
        # -------------------------------------------------

        if not cart_items:

            return redirect('home')

        # -------------------------------------------------
        # TEMPORARY DATA
        # -------------------------------------------------

        print("Name:", name)
        print("Phone:", phone)
        print("Email:", email)
        print("Address:", address)
        print("City:", city)
        print("State:", state)
        print("Pincode:", pincode)
        print("Payment:", payment)
        print("Total:", total)

        # -------------------------------------------------
        # CLEAR CART
        # -------------------------------------------------

        request.session['cart'] = {}
        request.session.modified = True

        return redirect('home')

    # =====================================================
    # CHECKOUT PAGE
    # =====================================================

    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(
        request,
        'checkout.html',
        context
    )


# =========================================================
# SUBCATEGORY PRODUCTS PAGE
# =========================================================

def subcategory_products(request, subcategory_id):

    subcategory = get_object_or_404(
        SubCategory,
        id=subcategory_id
    )

    # Only selected subcategory products
    products = Product.objects.filter(
        subcategory=subcategory,
        available=True
    ).select_related(
        'category',
        'subcategory'
    ).order_by('-created_at')

    context = {
        'subcategory': subcategory,
        'category': subcategory.category,
        'products': products,
    }

    return render(
        request,
        'subcategory_products.html',
        context
    )


# =========================================================
# SEARCH PRODUCTS
# =========================================================

def search_products(request):

    query = request.GET.get(
        'q',
        ''
    ).strip()

    products = Product.objects.none()

    if query:

        products = Product.objects.filter(

            Q(name__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query) |
            Q(color__icontains=query) |
            Q(category__name__icontains=query),

            available=True

        ).select_related(
            'category',
            'subcategory'
        ).order_by(
            '-created_at'
        )

    context = {
        'products': products,
        'query': query,
    }

    return render(
        request,
        'search_results.html',
        context
    )


# =========================================================
# SEARCH SUGGESTIONS
# =========================================================

def search_suggestions(request):

    query = request.GET.get(
        'q',
        ''
    ).strip()

    if len(query) < 2:

        return JsonResponse({
            'products': []
        })

    products = Product.objects.filter(

        Q(name__icontains=query) |
        Q(category__name__icontains=query) |
        Q(color__icontains=query),

        available=True

    ).select_related(
        'category'
    ).order_by(
        '-created_at'
    )[:6]

    data = []

    for product in products:

        image_url = ''

        if product.image:
            image_url = product.image.url

        data.append({

            'id': product.id,

            'name': product.name,

            'price': str(product.price),

            'category': product.category.name,

            'image': image_url,

            'url': f'/product/{product.id}/',

        })

    return JsonResponse({
        'products': data
    })


# =========================================================
# SHOES PAGE
def shoes(request):
    shoes_products = Product.objects.filter(
        category__name__iexact="Shoes",
        available=True
    ).select_related(
        "category",
        "subcategory"
    ).order_by("-created_at")

    return render(
        request,
        "shoes.html",
        {
            "shoes_products": shoes_products
        }
    )
# =========================================================
# MAKEUP PAGE
# =========================================================

def makeup(request):

    makeup_products = Product.objects.filter(

        category__name__iexact="Makeup",

        available=True

    ).select_related(
        "category",
        "subcategory"
    ).order_by(
        "-id"
    )

    return render(
        request,
        "makeup.html",
        {
            "makeup_products": makeup_products
        }
    )


# =========================================================
# ELECTRONICS PAGE
# =========================================================

def electronics(request):

    electronics_products = Product.objects.filter(

        category__name__iexact="Electronics",

        available=True

    ).select_related(
        "category",
        "subcategory"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "electronics.html",
        {
            "electronics_products": electronics_products
        }
    )


# =========================================================
# WATCHES PAGE
# =========================================================

def watches(request):

    watches_products = Product.objects.filter(

        category__name__iexact="Watches",

        available=True

    ).select_related(
        "category",
        "subcategory"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "watches.html",
        {
            "watches_products": watches_products
        }
    )



def accessories(request):

    accessories_products = Product.objects.filter(

        category__name__iexact="Accessories",

        available=True

    ).select_related(
        "category",
        "subcategory"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "Accessories.html",
        {
            "accessories_products": accessories_products
        }
    )
    
    
    
    
    
    
    
    
    
    
    
    
def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        if not all([name, email, subject, message_text]):
            messages.error(
                request,
                'Please fill in all fields.'
            )
        elif len(name) > 100 or len(subject) > 200:
            messages.error(
                request,
                'Name or subject is too long.'
            )
        else:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message_text
            )

            messages.success(
                request,
                'Thank you! Your message has been submitted successfully.'
            )
            return redirect('contact')

    return render(request, 'contact.html')