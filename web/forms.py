from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Product, Seller, ProductVariant, ContactMessage  # Make sure to import Seller
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# -------------------- NewsletterSubscription Form --------------------
from django import forms
from .models import NewsletterSubscription

class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Your email address', 'required': True}),
        }

# -------------------- Product Form --------------------
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Product

class ProductForm(forms.ModelForm):
    product_description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = ['name', 'category', 'short_description', 'product_description', 'image']

# -------------------- Contact Form --------------------

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'subject': forms.TextInput(attrs={'class': 'input'}),
            'message': forms.Textarea(attrs={'class': 'textarea'}),
        }
# -------------------- Signup Form --------------------
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data


# -------------------- Login Form --------------------
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# -------------------- Seller Registration Form --------------------
class SellerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['store_name', 'phone_number', 'address']
        widgets = {
            'store_name': forms.TextInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'}),
            'phone_number': forms.TextInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'}),
            'address': forms.Textarea(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(SellerRegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True




# -------------------- Product Variant Form --------------------
class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['unit', 'size', 'product_price', 'product_stock', 'delivery_price']  # Include 'delivery_price'
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'product_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'product_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'delivery_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),  # Make sure this is included in the form
        }

# web/forms.py
from django import forms

class AddressForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter your address', 'rows': 4, 'cols': 50}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))
