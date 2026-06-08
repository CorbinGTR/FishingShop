from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("orders/", views.orders, name="orders"),
    path("admin-panel/", views.admin_dashboard, name="admin_dashboard"),
    path("panel/products/", views.admin_products, name="admin_products"),
    path("panel/products/add/", views.admin_product_add, name="admin_product_add"),
    path(
        "panel/products/edit/<int:product_id>/",
        views.admin_product_edit,
        name="admin_product_edit",
    ),
    path(
        "panel/products/delete/<int:product_id>/",
        views.admin_product_delete,
        name="admin_product_delete",
    ),
    path("panel/categories/", views.admin_categories, name="admin_categories"),
    path("panel/orders/", views.admin_orders, name="admin_orders"),
    path(
        "panel/orders/<int:order_id>/",
        views.admin_order_detail,
        name="admin_order_detail",
    ),
    path("panel/users/", views.admin_users, name="admin_users"),
]
