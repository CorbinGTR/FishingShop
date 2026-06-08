from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .forms import OrderForm, RegisterForm, ProductForm, CategoryForm
from .models import Category, Product, Order, OrderItem


def staff_required(user):
    return user.is_staff


def get_cart(request):
    return request.session.setdefault("cart", {})


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    category_id = request.GET.get("category")
    search = request.GET.get("search")
    if category_id:
        products = products.filter(category_id=category_id)

    if search:
        products = products.filter(name__icontains=search)

    return render(
        request,
        "product_list.html",
        {
            "categories": categories,
            "products": products,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, "product_detail.html", {"product": product})


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    cart = get_cart(request)
    product_id = str(product.id)
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session.modified = True
    return redirect("shop:cart_detail")


def cart_remove(request, product_id):
    cart = get_cart(request)
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]
        request.session.modified = True

    return redirect("shop:cart_detail")


def cart_detail(request):
    cart = get_cart(request)
    items = []
    total_price = Decimal("0")
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        total_price += item_total
        items.append(
            {
                "product": product,
                "quantity": quantity,
                "total": item_total,
            }
        )

    return render(
        request,
        "cart.html",
        {
            "items": items,
            "total_price": total_price,
        },
    )


def checkout(request):
    cart = get_cart(request)
    if not cart:
        return redirect("shop:cart_detail")

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user

            order.save()
            for product_id, quantity in cart.items():
                product = get_object_or_404(Product, id=product_id)

                OrderItem.objects.create(
                    order=order, product=product, price=product.price, quantity=quantity
                )

            request.session["cart"] = {}
            return render(request, "order_success.html", {"order": order})
    else:
        form = OrderForm()

    return render(request, "checkout.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("shop:product_list")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("shop:product_list")
    else:
        form = AuthenticationForm()

    form.fields["username"].widget.attrs.update(
        {"class": "form-control", "placeholder": "Введите логин"}
    )

    form.fields["password"].widget.attrs.update(
        {"class": "form-control", "placeholder": "Введите пароль"}
    )

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("shop:product_list")


@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders.html", {"orders": orders})


@user_passes_test(staff_required, login_url="/login/")
def admin_dashboard(request):
    return render(
        request,
        "admin/dashboard.html",
        {
            "products_count": Product.objects.count(),
            "orders_count": Order.objects.count(),
            "users_count": User.objects.count(),
        },
    )


@user_passes_test(staff_required, login_url="/login/")
def admin_products(request):
    products = Product.objects.all()
    return render(request, "admin/products.html", {"products": products})


@user_passes_test(staff_required, login_url="/login/")
def admin_product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("shop:admin_products")
    else:
        form = ProductForm()

    return render(
        request,
        "admin/product_form.html",
        {"form": form, "title": "Добавить товар"},
    )


@user_passes_test(staff_required, login_url="/login/")
def admin_product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("shop:admin_products")
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "admin/product_form.html",
        {"form": form, "title": "Редактировать товар"},
    )


@user_passes_test(staff_required, login_url="/login/")
def admin_product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect("shop:admin_products")


@user_passes_test(staff_required, login_url="/login/")
def admin_categories(request):
    categories = Category.objects.all()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("shop:admin_categories")
    else:
        form = CategoryForm()

    return render(
        request,
        "admin/categories.html",
        {
            "categories": categories,
            "form": form,
        },
    )


@user_passes_test(staff_required, login_url="/login/")
def admin_orders(request):
    orders = Order.objects.all()
    return render(request, "admin/orders.html", {"orders": orders})


@user_passes_test(staff_required, login_url="/login/")
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.status = request.POST.get("status")
        order.save()
        return redirect("shop:admin_order_detail", order_id=order.id)

    return render(request, "admin/order_detail.html", {"order": order})


@user_passes_test(staff_required, login_url="/login/")
def admin_users(request):
    users = User.objects.all()
    return render(request, "admin/users.html", {"users": users})
