from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static
from web.views import index, product, products, cart_view, loginsignup, add_product, search_results, \
      seller_dashboard, profile_view, orders_view, error,add_to_cart, contact_view
from . import views
                    



app_name = 'web'

urlpatterns = [
    path("", index, name='index'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    path('profile/', profile_view, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('orders/', orders_view, name='orders'),
    path('about/', views.about, name='about'),


    path("product_detail/<pk>/", product, name='product'),
    path("add-product/", add_product, name="add_product"),
    path("products/", products, name='products'),
    path("cart/", cart_view, name='cart'),
    path('remove-cart-item/', views.remove_cart_item, name='remove_cart_item'),

    path("login-signup/", loginsignup, name='login-signup'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_view, name='account'),
    path('accounts/login/', loginsignup, name='login'),
    path('', views.account_view, name='index'),

    path('seller/my-products/', views.my_products, name='my_products'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),  # ✅ Add this line
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    
    path('search/', search_results, name='search_results'),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('become-seller/', views.become_seller, name='become_seller'),
    path('seller-dashboard/', seller_dashboard, name='seller_dashboard'),
    
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),

    path('checkout/', views.checkout, name='checkout'),  # your checkout page
    path('add-address/', views.add_address, name='add_address'),
    path('payment/', views.payment, name='payment'),
    path('create_order/', views.create_order, name='create_order'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('seller/orders/', views.seller_orders, name='seller_orders'),
    path('order/<int:order_id>/', views.order_details, name='order_details'),  # Seller order details
    path('user/order/<int:order_id>/', views.user_order_details, name='user_order_details'),  # User order details
    path('seller/order/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('user/orders/', views.user_orders, name='user_orders'),  # List of user's orders
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('contact/', contact_view, name='contact'),
    path('newsletter/', views.newsletter_subscription_view, name='newsletter_subscription'),

    
    path('404/', error, name='error'),
    
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)