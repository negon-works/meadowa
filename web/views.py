import json
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from fuzzywuzzy import fuzz
from django.db.models import Min
from .models import Product, ProductVariant,Seller,CartItem,Profile,NewsletterSubscription
from .forms import ProductForm, SignupForm,SellerRegistrationForm, ContactForm, NewsletterSubscriptionForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ShippingAddress

@login_required
def profile_view(request):
    user = request.user
    seller_status = None
    if hasattr(user, 'seller_profile'):
        seller_status = user.seller_profile.status
    
    addresses = ShippingAddress.objects.filter(user=user)

    # Handle address deletion
    if request.method == 'POST' and 'delete_address' in request.POST:
        address_id = request.POST.get('address_id')
        try:
            address = ShippingAddress.objects.get(id=address_id, user=user)
            address.delete()
        except ShippingAddress.DoesNotExist:
            pass  # Handle if address doesn't exist or any other logic

        return redirect('web:profile')  # Redirect to the same page after deletion
    
    return render(request, 'profile.html', {
        'seller_status': seller_status,
        'addresses': addresses,
    })
@login_required
def profile_settings(request):
    return render(request, 'profile_settings.html')


@login_required
def orders_view(request):
    return render(request, 'orders.html')

# Home page view
from django.db.models import Min

from django.shortcuts import render
from django.db.models import Min
from .models import Product
def privacy_policy(request):
    return render(request, 'privacy.html')
def index(request):
    # Fetch products with their minimum price from variants
    products = Product.objects.annotate(min_price=Min('variants__product_price')).distinct()

    # Filter products by category
    dairy_products = products.filter(category="Dairy")
    poultry_products = products.filter(category="Poultry")
    farm_produce = products.filter(category="Fruits & Vegs")
    beverages = products.filter(category="Juices & Honeys")

    # Pass the filtered products and categories to the template
    context = {
        "products": products,
        "dairy_products": dairy_products,
        "poultry_products": poultry_products,
        "farm_produce": farm_produce,
        "beverages": beverages,
    }
    return render(request, "index.html", context)



def error(request):
    return render (request,'404error.html')
def about(request):
    return render (request,'about.html')
def contact_view(request):
    initial_data = {
        'subject': request.GET.get('subject', ''),
        'name': request.GET.get('name', request.user.username if request.user.is_authenticated else ''),
        'email': request.GET.get('email', request.user.email if request.user.is_authenticated else ''),
    }

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for contacting us! We'll get back to you soon.")
            return redirect('web:contact')
    else:
        form = ContactForm(initial=initial_data)

    return render(request, 'contact.html', {'form': form})



@require_POST
def newsletter_subscription_view(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        email = request.POST.get('email')

        if email:
            # Check if already subscribed
            if NewsletterSubscription.objects.filter(email=email).exists():
                return JsonResponse({'message': 'You are already subscribed!'}, status=400)

            form = NewsletterSubscriptionForm({'email': email})
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Thanks for subscribing! We\'ll keep you updated.'})
            else:
                return JsonResponse({'message': 'Invalid email address! Please try again.'}, status=400)

        return JsonResponse({'message': 'Email address is required!'}, status=400)
    
    return JsonResponse({'message': 'Invalid request'}, status=400)
# Product detail page
from django.core.cache import cache 
from django.db.models import F, Q, Sum, Count # Optional if you want time-limited deduplication


def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    variants = product.variants.all()

    user = request.user
    is_seller = user.is_authenticated and hasattr(user, 'seller_profile') and product.seller == user.seller_profile

    # Generate a unique key per user/session per product
    if user.is_authenticated:
        user_key = f"viewed_product_{product.id}_user_{user.id}"
    else:
        user_key = f"viewed_product_{product.id}_session_{request.session.session_key}"
        if not request.session.session_key:
            request.session.create()

    # Check if this user/session has already viewed it
    if not is_seller and not cache.get(user_key):
        product.views = F('views') + 1
        product.save(update_fields=['views'])
        cache.set(user_key, True, timeout=60 * 60 * 12)  # 12 hours

    return render(request, 'product_detail.html', {
        'product': product,
        'variants': variants,
        'seller': product.seller  # Adding the seller info
    })



# All products view
from django.db.models import Min
from .models import Product

def products(request):
    products = Product.objects.annotate(min_price=Min('variants__product_price')).distinct()

    # Get category choices from the model
    category_choices = [choice[0] for choice in Product.CATEGORY_CHOICES]

    return render(request, 'products.html', {
        'products': products,
        'categories': category_choices  # Pass choices to template
    })




from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Product, ProductVariant
from django.db.models import Min

@login_required
def my_products(request):
    if not hasattr(request.user, 'seller_profile'):
        return redirect('web:profile')

    seller = request.user.seller_profile
    products = Product.objects.filter(seller=seller)
    return render(request, 'my_products.html', {'products': products})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user.seller_profile)
    variants = product.variants.all()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller_profile
            product.product_description = request.POST.get('product_description', '')
            product.save()

            sizes = request.POST.getlist('size')
            prices = request.POST.getlist('price')
            stocks = request.POST.getlist('stock')
            units = request.POST.getlist('unit')
            delivery_prices = request.POST.getlist('delivery_price')  # 👈 Added this line

            product.variants.all().delete()

            for i in range(len(sizes)):
                size = sizes[i]
                price = prices[i]
                stock = stocks[i]
                unit = units[i]
                delivery_price = delivery_prices[i] if i < len(delivery_prices) else 0

                if size and price and stock:
                    ProductVariant.objects.create(
                        product=product,
                        size=size,
                        product_price=price,
                        product_stock=stock,
                        unit=unit,
                        delivery_price=delivery_price  # 👈 Save it here too
                    )

            return redirect('web:my_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {
        'form': form,
        'editing': True,
        'product': product,
        'variants': variants
    })




@csrf_exempt  # we'll handle CSRF manually
@login_required
def delete_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id, seller=request.user.seller_profile)
        product.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})



# Add product page view
def add_product(request):
    if request.method == "POST":
        print("📝 Received POST Request")
        print("Form Data:", request.POST)
        print("Files Data:", request.FILES)

        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Save product but without committing to DB to manually add description
            product = form.save(commit=False)
            
            # Save the product description (ensure it's stored as HTML)
            product.product_description = request.POST.get('product_description', '')
            product.seller = request.user.seller_profile
            product.save()
  # Now save with description
            
            print(f"✅ Product '{product.name}' added successfully!")

            # Add product variants
            sizes = request.POST.getlist('size[]')
            prices = request.POST.getlist('price[]')
            stocks = request.POST.getlist('stock[]')
            units = request.POST.getlist('unit[]')
            delivery_prices = request.POST.getlist('delivery_price[]')

            for i in range(len(sizes)):
                if sizes[i] and prices[i] and stocks[i] and units[i] and delivery_prices[i]:
                    ProductVariant.objects.create(
                        product=product,
                        size=sizes[i],
                        product_price=prices[i],
                        product_stock=stocks[i],
                        unit=units[i],
                        delivery_price=delivery_prices[i],
                    )
            print("✅ Variants added successfully!")
            return redirect('web:products')  # Redirect to the products list page after saving
        else:
            print("❌ Form not valid:", form.errors)
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})



def search_results(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()

    matched_products = []
    if query:
        # ✅ Match products by name using fuzzy search
        for product in products:
            score = fuzz.partial_ratio(query.lower(), product.name.lower())
            
            # ✅ Consider a match if score >= 60
            if score >= 60:
                product.min_price = product.get_min_price()
                matched_products.append(product)

        # ✅ Search for matching categories
        category_products = Product.objects.filter(category__icontains=query)
        for product in category_products:
            product.min_price = product.get_min_price()
            if product not in matched_products:  # Avoid duplicates
                matched_products.append(product)

    # ✅ Check if no matches found
    no_results_found = not matched_products and query

    if no_results_found:
        # ✅ Show all products if no results are found
        all_products = Product.objects.all()
        for product in all_products:
            product.min_price = product.get_min_price()
    else:
        all_products = None

    context = {
        'products': matched_products,
        'query': query,
        'no_results_found': no_results_found,
        'all_products': all_products,
    }
    return render(request, 'search.html', context)



def account_view(request):
    if request.user.is_authenticated:
        return redirect('web:index')  # If already logged in, redirect to homepage.

    if request.method == 'POST':
        if 'signup_form' in request.POST:  # Handle Signup
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                username = signup_form.cleaned_data['username']
                email = signup_form.cleaned_data['email']

                # Check if username or email is already taken
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already taken. Please choose another one.")
                    return redirect('web:account')
                
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email is already registered. Try logging in.")
                    return redirect('web:account')

                # If unique, save the user
                try:
                    user = signup_form.save(commit=False)
                    user.set_password(signup_form.cleaned_data['password'])
                    user.save()
                    login(request, user)
                    messages.success(request, "Account created successfully!")
                    return redirect('web:index')  # Redirect to home page after signup
                except IntegrityError:
                    messages.error(request, "Something went wrong. Please try again.")
                    return redirect('web:account')

        elif 'login_form' in request.POST:  # Handle Login
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")

                # After login, check if there's a next parameter and redirect accordingly
                next_url = request.GET.get('next', 'web:index')  # Default to index if no next param
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
                
    return render(request, 'login-signup.html')



def logout_view(request):
    logout(request)
    return redirect('/')

# Cart page view
def cart(request):
    return render(request, 'cart.html')

# Login and Signup page view
def loginsignup(request):
    return render(request, 'login-signup.html')

def seller_register(request):
    return render(request, 'seller-register.html')


from datetime import date, timedelta
from django.db.models import Sum, F
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models.functions import TruncDate

@login_required
def seller_dashboard(request):
    if not hasattr(request.user, 'seller_profile'):
        messages.warning(request, "Access denied. You are not registered as a seller.")
        return redirect('web:profile')

    seller = request.user.seller_profile

    if seller.status == 'pending':
        messages.info(request, "Your seller account is still under review.")
        return redirect('web:profile')
    elif seller.status == 'rejected':
        messages.error(request, "Access denied. Your seller account was rejected. Please contact support.")
        return redirect('web:profile')

    order_items = OrderItem.objects.filter(product__seller=seller).select_related('order')

    recent_orders_qs = Order.objects.filter(
        id__in=order_items.values_list('order_id', flat=True)
    ).order_by('-ordered_at')[:5]

    recent_orders = []
    for order in recent_orders_qs:
        item = order.order_items.filter(product__seller=seller).first()
        recent_orders.append({
            'id': order.id,
            'customer_name': order.user.get_full_name() or order.user.username,
            'amount': item.product_price * item.quantity + item.delivery_price,
            'status': order.order_status.replace('_', ' ').capitalize(),
            'status_color': status_color_map(order.order_status),
            'date': order.ordered_at.strftime("%b %d, %Y"),
        })

    total_sales = Order.objects.filter(
        order_items__product__seller=seller,
        order_status='delivered'
    ).aggregate(total_sales=Sum('grand_total'))['total_sales'] or 0

    total_orders = Order.objects.filter(
        order_items__product__seller=seller
    ).count()

    pending_orders = Order.objects.filter(
        order_items__product__seller=seller,
        order_status='pending'
    ).count()

    product_views = Product.objects.filter(seller=seller).aggregate(total_views=Sum('views'))['total_views'] or 0

    # -------------------------
    # 📊 Chart Data (Last 7 days)
    today = date.today()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

    daily_sales_data = (
        OrderItem.objects
        .filter(product__seller=seller, order__ordered_at__date__gte=today - timedelta(days=6))
        .annotate(order_date=TruncDate('order__ordered_at'))
        .values('order_date')
        .annotate(total_sales=Sum(F('product_price') * F('quantity') + F('delivery_price')))
        .order_by('order_date')
    )

    sales_chart_data = {day: 0 for day in last_7_days}

    # Populate the sales data for the chart
    for item in daily_sales_data:
        sales_chart_data[item['order_date']] = float(item['total_sales'])

    # Label for chart (e.g., Apr 15, Apr 16, etc.)
    chart_labels = [day.strftime('%b %d') for day in last_7_days]
    
    # Sales values (total sales for each of the last 7 days)
    chart_values = [sales_chart_data[day] for day in last_7_days]

    # -------------------------
    context = {
        'recent_orders': recent_orders,
        'total_sales': total_sales,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'product_views': product_views,
        'chart_labels': chart_labels,
        'chart_values': chart_values,
    }

    return render(request, 'seller_dashboard.html', context)


def status_color_map(status):
    return {
        'pending': 'yellow-500',
        'confirmed': 'blue-500',
        'shipped': 'indigo-500',
        'out_of_delivery': 'purple-500',
        'delivered': 'green-500',
    }.get(status, 'gray-500')







# This decorator ensures that users must be logged in to access the page
@login_required
def become_seller(request):
    # 🛡️ Check if the user already has a seller profile before accessing it
    if hasattr(request.user, 'seller_profile'):
        if request.user.seller_profile.status == 'pending':
            messages.info(request, 'You have already submitted your seller application for review.')
            return redirect('web:profile')

    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            seller = form.save(commit=False)
            seller.user = request.user
            seller.status = 'pending'
            seller.save()
            messages.success(request, 'Your seller application has been submitted for review!')
            return redirect('web:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SellerRegistrationForm()

    return render(request, 'seller/become_seller.html', {'form': form})



@csrf_exempt
@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            variant_id = data.get('variant_id')
            quantity = int(data.get('quantity', 1))
            subscription = data.get('subscription', 'none')

            product = Product.objects.get(id=product_id)
            variant = ProductVariant.objects.get(id=variant_id)

            # No need to add a separate 'size' field in CartItem if size is tied to ProductVariant
            size = variant.size  # Get the size from the variant

            # Check if item already in cart
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                variant=variant,
                defaults={
                    'product': product,
                    'quantity': quantity,
                    'subscription': subscription
                }
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.subscription = subscription
                cart_item.save()

            return JsonResponse({'message': 'Item added to cart successfully!'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)



@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('variant', 'product')

    total_price = 0
    total_delivery = 0
    for item in cart_items:
        item_price = item.variant.product_price * item.quantity
        delivery_charge = item.variant.delivery_price * item.quantity
        item_total = item_price + delivery_charge
        total_price += item_price
        total_delivery += delivery_charge

        # Store the item_total for each item to use in the template
        item.item_total = item_total

    grand_total = total_price + total_delivery

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_delivery': total_delivery,
        'grand_total': grand_total
    })



@require_POST
@login_required
def remove_cart_item(request):
    variant_id = request.POST.get('variant_id')
    if variant_id:
        try:
            cart_item = CartItem.objects.get(user=request.user, variant_id=variant_id)
            cart_item.delete()
            return JsonResponse({'success': True})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user

        # ensure profile exists
        profile, created = Profile.objects.get_or_create(user=user)

        # Update user details
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        # Update profile details
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')

        # Check for profile picture removal
        if request.POST.get('remove_pic'):
            profile.profile_pic = None

        # Check if a new profile picture is uploaded
        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']

        profile.save()

        return redirect('web:profile')  # or wherever your profile URL is
    
    def delete_product(request, pk):
        product = get_object_or_404(Product, pk=pk)
        if request.method == "POST":
            product.delete()
            return redirect('web:my_products')
        return render(request, 'web/confirm_delete.html', {'product': product})


from django.shortcuts import render, redirect
from .models import ShippingAddress, CartItem
from django.contrib.auth.decorators import login_required

@login_required
def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    
    total_price = sum(item.variant.product_price * item.quantity for item in cart_items)
    total_delivery = sum(item.variant.delivery_price for item in cart_items)
    grand_total = total_price + total_delivery

    addresses = ShippingAddress.objects.filter(user=user)
    default_address = addresses.first()

    # Get the selected address ID from the form (if available)
    selected_address_id = request.POST.get('selected_address_id', None)
    selected_address = ShippingAddress.objects.get(id=selected_address_id) if selected_address_id else default_address

    # Add item_total calculation for each cart item
    for item in cart_items:
        item.item_total = (item.variant.product_price * item.quantity) + item.variant.delivery_price

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_delivery': total_delivery,
        'grand_total': grand_total,
        'addresses': addresses,
        'default_address': default_address,
        'selected_address': selected_address,
    })



from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import ShippingAddress

@login_required
def add_address(request):
    if request.method == "POST":
        name = request.POST.get("name")
        house = request.POST.get("house_address")
        street = request.POST.get("street")
        city = request.POST.get("city")
        district = request.POST.get("district")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        phone = request.POST.get("phone")
        address_type = request.POST.get("address_type")
        custom_type = request.POST.get("custom_type")

        if address_type == "other":
            address_type = custom_type or "Other"

        ShippingAddress.objects.create(
            user=request.user,  # ✅ THIS IS THE IMPORTANT FIX
            name=name,
            house_address=house,
            street=street,
            city=city,
            district=district,
            state=state,
            pincode=pincode,
            phone=phone,
            address_type=address_type
        )
        return redirect("web:checkout")  # redirect to your checkout or address page

    return redirect("web:checkout")  # fallback





@login_required
def payment(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        if payment_method == 'cod':
            return redirect('web:order_confirmation')
    return redirect('web:checkout')

@login_required
def order_confirmation(request):
    return render(request, 'order_confirmation.html')

# views.py


from django.http import Http404
from django.db import transaction
from django.shortcuts import redirect
from .models import CartItem, ShippingAddress, Order, OrderItem
from django.contrib.auth.decorators import login_required

import logging
from django.http import Http404
from django.shortcuts import redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required

# Create a logger
logger = logging.getLogger(__name__)

@login_required
def create_order(request):
    if request.method != 'POST':
        raise Http404("Invalid request")

    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    if not cart_items.exists():
        return redirect('web:cart')

    selected_address_id = request.POST.get('selected_address_id')
    if not selected_address_id:
        raise Http404("No shipping address selected.")

    try:
        shipping_address = ShippingAddress.objects.get(id=selected_address_id, user=user)
    except ShippingAddress.DoesNotExist:
        raise Http404("Invalid shipping address.")

    total_price = sum(item.variant.product_price * item.quantity for item in cart_items)
    total_delivery = sum(item.variant.delivery_price for item in cart_items)
    grand_total = total_price + total_delivery

    with transaction.atomic():
        # Create the order
        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address,
            total_price=total_price,
            delivery_price=total_delivery,
            grand_total=grand_total
        )

        # Log the order creation
        logger.info(f"Order created: {order.id}")

        # Iterate through cart items and create order items
        for item in cart_items:
            logger.info(f"CartItem details: product={item.product.name}, variant={item.variant.size}, quantity={item.quantity}")

            order_item = OrderItem.objects.create(
                order=order,
                product=item.product,
                variant=item.variant,
                quantity=item.quantity,
                product_price=item.variant.product_price,
                delivery_price=item.variant.delivery_price
            )


            # Log the order item creation
            logger.info(f"OrderItem created: {order_item.product.name} x{order_item.quantity}")

        # Delete cart items after order is created
        cart_items.delete()

    return redirect('web:order_confirmation')





# views.py

@login_required
def seller_orders(request):
    # Check if user has a seller profile
    if not hasattr(request.user, 'seller_profile'):
        return redirect('web:profile')  # Or wherever you want to redirect non-sellers

    seller = request.user.seller_profile

    # Fetch only orders that include this seller's products
    orders = Order.objects.filter(
        order_items__product__seller=seller
    ).distinct().prefetch_related('order_items__product', 'shipping_address')

    return render(request, 'seller_orders.html', {'orders': orders})

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import Order  # adjust import if needed

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import Order

@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    try:
        seller = request.user.seller_profile  # Get seller using correct related_name
    except ObjectDoesNotExist:
        return redirect('web:seller_orders')  # User is not a seller

    # Make sure all products in this order belong to this seller
    if not all(item.product.seller == seller for item in order.order_items.all()):
        return redirect('web:seller_orders')  # Unauthorized seller

    if request.method == 'POST':
        new_status = request.POST.get('order_status')

        valid_statuses = ['confirmed', 'shipped', 'out_for_delivery', 'delivered']
        if new_status not in valid_statuses:
            return redirect('web:seller_orders')

        if order.order_status != new_status:
            order.order_status = new_status
            order.status_updated_at = timezone.now()
            order.save()

        return redirect('web:seller_orders')

    return redirect('web:seller_orders')




# views.py

@login_required
def order_details(request, order_id):
    order = Order.objects.get(id=order_id)

    return render(request, 'order_details.html', {'order': order})

# views.py

@login_required
def user_order_details(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.user != order.user:
        return redirect('web:index')  # Prevent access to orders that are not theirs

    # Define the steps in the progress (with underscores for consistency)
    status_order = ['pending', 'confirmed', 'shipped', 'out_for_delivery', 'delivered']
    progress = []

    # Normalize the order status to match the format in status_order (replace spaces with underscores)
    order_status_normalized = order.order_status.replace(' ', '_').lower()

    # Ensure the status is normalized correctly
    if order_status_normalized not in status_order:
        raise ValueError(f"Unexpected status '{order_status_normalized}' in order {order.id}")

    # Loop through each status and determine if it's completed based on the order status
    for status in status_order:
        # Ensure both the status and order status are in the same format
        is_completed = status_order.index(status) <= status_order.index(order_status_normalized)
        progress.append({
            'name': status.replace('_', ' ').capitalize(),  # Display status in readable format
            'completed': is_completed,
            'is_first': (status == status_order[0]),  # Mark the first step as special
        })

    # Calculate the total for each item in the order
    for item in order.order_items.all():
        item.total_price = item.quantity * item.product_price  # Add the total_price for each item

    return render(request, 'user_order_details.html', {'order': order, 'progress': progress})




@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')
    return render(request, 'user_orders.html', {'orders': orders})

