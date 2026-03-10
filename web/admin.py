from django.contrib import admin
from .models import Product, ProductVariant, CartItem, Seller, Order, OrderItem ,\
ContactMessage


admin.site.site_header = "Meadowa"
admin.site.site_title = "Meadowa Admin Portal"
admin.site.index_title = "Welcome to Meadowa Admin Portal"
# Inline admin for product variants
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1  # show 1 empty variant field by default
    min_num = 1
    verbose_name = "Size Variant"
    verbose_name_plural = "Size Variants"

# Product admin with inline
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'short_description')
    inlines = [ProductVariantInline]  # <-- This adds the variants directly in Product admin

# Registering other models
@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['user', 'store_name', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['user__username', 'store_name']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'variant', 'quantity', 'subscription', 'added_at']
    search_fields = ['user__username', 'product__name', 'variant__size']
    list_filter = ['subscription']

# Register ProductAdmin
admin.site.register(Product, ProductAdmin)

# Admin for OrderItem Inline in Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'variant', 'quantity', 'product_price', 'delivery_price']
    can_delete = False

# Admin for Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_status', 'grand_total', 'ordered_at', 'get_shipping_address']
    list_filter = ['order_status', 'ordered_at']
    search_fields = ['user__username', 'id']
    inlines = [OrderItemInline]

    def get_shipping_address(self, obj):
        return obj.shipping_address.full_address if obj.shipping_address else "Address not available"
    get_shipping_address.short_description = 'Shipping Address'



# Admin for OrderItem

from django.contrib import admin
from .models import OrderItem

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'variant', 'quantity', 'product_price', 'delivery_price']
    search_fields = ['product__name', 'variant__size', 'order__id']
    list_filter = ['order__ordered_at']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
    search_fields = ('name', 'email', 'subject')

# models.py
# admin.py
from django.contrib import admin
from .models import NewsletterSubscription

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed')
    search_fields = ('email',)
    list_filter = ('date_subscribed',)

