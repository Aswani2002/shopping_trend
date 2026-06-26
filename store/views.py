from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import UserData
from .models import Product
from .models import Order




def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Account created successfully. Please login.')
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ✅ Use authenticate() properly
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # ✅ pass user object, not username string
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def buynow(request):
    return render(request, 'buynow.html')

def payment_view(request):
    return render(request, 'payment.html')
def cart_view(request):
    return render(request, 'cart.html')

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"
ADMIN_USER_ID = 1


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('admin_username')
        password = request.POST.get('admin_password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            request.session['admin_logged_in'] = True
            request.session['admin_username'] = ADMIN_USERNAME
            request.session['admin_user_id'] = ADMIN_USER_ID
            return redirect('admin_home')
        else:
            messages.error(request, "Invalid admin credentials!")

    return render(request, 'admin/admin_login.html')


def admin_home(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    users = UserData.objects.all()
    orders = Order.objects.all()
    
    total_users = users.count()
    total_products = Product.objects.count()
    total_orders = orders.count()
    
    # Calculate total sales amount
    total_sales = sum(float(order.total) for order in orders)
    
    return render(request, 'admin/admin_home.html', {
        'Users': users, 
        'total_users': total_users, 
        'total_products': total_products, 
        'total_orders': total_orders,
        'total_sales': total_sales
    })



def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        Product.objects.create(
            name=name,
            price=price,
            description=description,
            image=image
        )
    products=Product.objects.all()
    return render(request, "admin/add_product.html",{'products':products})

def delete(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('add_product')

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_details.html', {'product': product})



def payment(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to proceed with payment.")
        return redirect('login')
    
    product_obj = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        # Get address data from the form
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        
        # Update user profile with address
        user_data = UserData.objects.filter(user=request.user).first()
        
        if user_data:
            # User already has a profile, update it
            user_data.phone = phone
            user_data.first_name = full_name.split()[0] if full_name else ''
            user_data.last_name = ' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
            # Only update email if it's different and doesn't exist elsewhere
            if user_data.email != email:
                if UserData.objects.filter(email=email).exclude(id=user_data.id).exists():
                    messages.error(request, "This email is already registered with another account.")
                    return redirect('payment', id=id)
                user_data.email = email
            user_data.save()
        else:
            # Create new profile - check if email already exists
            if UserData.objects.filter(email=email).exists():
                messages.error(request, "This email is already registered. Please use a different email.")
                return redirect('payment', id=id)
            
            user_data = UserData.objects.create(
                user=request.user,
                email=email,
                phone=phone,
                first_name=full_name.split()[0] if full_name else '',
                last_name=' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
            )
        
        # Create order
        quantity = int(request.POST.get('quantity', 1))
        total_price = float(product_obj.price) * quantity
        
        order = Order.objects.create(
            customer=request.user,
            old_customer_name=full_name,
            product_name=product_obj.name,
            quantity=quantity,
            price=float(product_obj.price),
            total=total_price,
            payment_status="Success",
            address=f"{address}, {city}, {state}, {pincode}",
            phone=phone
        )
        
        messages.success(request, "Payment successful! Your order has been placed.")
        return redirect('index')
    
    return render(request, "payment.html", {"Product": product_obj})



def admin_orders(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    orders = Order.objects.all().order_by('-order_date')
    return render(request, "admin/admin_orders.html", {"orders": orders})
