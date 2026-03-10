from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class Seller(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    store_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"
    
class Product(models.Model):
    UNIT_CHOICES = [
        ('ml', 'Milliliters'),
        ('l', 'Liters'),
        ('g', 'Grams'),
        ('kg', 'Kilograms'),
        ('packet', 'Packet'),
        ('bottle', 'Bottle'),
    ]

    CATEGORY_CHOICES = [
        ('Dairy', 'Dairy Products'),
        ('Poultry', 'Poultry Products'),
        ('Fruits & Vegs', 'Fruits & Vegs'),
        ('Juices & Honeys', 'Juices & Honeys'),
    ]

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Dairy')
    short_description = models.CharField(max_length=100)
    product_description = RichTextField()
    image = models.FileField(upload_to='products/main_images')
    views = models.PositiveIntegerField(default=0)  # Add this field to track views

    class Meta:
        db_table = "web_product"
        ordering = ["id"]

    def __str__(self):
        return self.name

    def get_min_price(self):
        min_price = self.variants.aggregate(min_price=models.Min('product_price'))['min_price']
        return min_price if min_price else 0


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    unit = models.CharField(max_length=10, choices=Product.UNIT_CHOICES)
    size = models.CharField(max_length=50)
    product_price = models.DecimalField(max_digits=10, decimal_places=2,default=10 )
    product_stock = models.PositiveIntegerField(default=0)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product.name} - {self.size}"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subscription = models.CharField(max_length=20, choices=[
        ('none', 'One-time Purchase'),
        ('daily', 'Daily Delivery')
    ], default='none')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'variant')

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.variant.size})"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    pincode = models.CharField(max_length=6, blank=True)  # 6-digit pincode
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class ShippingAddress(models.Model):
    ADDRESS_TYPES = (
        ('home', 'Home'),
        ('workplace', 'Workplace'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_addresses')
    name = models.CharField(max_length=100)
    house_address = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='home')
    label = models.CharField(max_length=100, blank=True, null=True)  # for 'Other' address type
    is_default = models.BooleanField(default=False)  # New field to mark the default address
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_address_type_display()}) - {self.house_address}, {self.city}"

    def full_address(self):
        label_part = f"{self.label}, " if self.address_type == 'other' and self.label else ""
        return (
            f"{self.name}, {self.house_address}, {self.street}, "
            f"{self.city}, {self.district}, {self.state} - {self.pincode}, "
            f"{label_part}Phone: {self.phone}"
        )


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('out_of_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    status_updated_at = models.DateTimeField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_at = models.DateTimeField(default=datetime.now)
    
    def save(self, *args, **kwargs):
    # No logic, just save it
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    

# models.py
from django.db import models

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

