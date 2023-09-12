from django import forms

from .models import Catagory, Brand, Price_Filter, Size,Coupon,Product,User


class CreateShopForm(forms.ModelForm):
    repassword = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username','email','password','repassword','shopname','address','contact_number']


class UpdateShopForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['shopname']

class ChangePassword(forms.Form):
    oldpass = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    newpass = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirmpass = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))  

class Checkout(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))

class LoginForm(forms.Form):
    loginusername=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    loginpassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['catagory', 'name', 'desc', 'price','quantity', 'img', 'brand', 'price_filter','color','size', 'discount']
    
        
      
class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['catagory', 'name', 'desc', 'price','quantity', 'brand', 'price_filter','size', 'discount']
    

class SignupCustomer(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    repassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
   
class SignupShop(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    repassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    shopname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contactnum = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))

class CouponUpdateForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['coupon_code', 'discount_price', 'minimum_amount', 'is_expired']
    
   
class CouponCreateForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['coupon_code', 'discount_price', 'minimum_amount', 'is_expired']
    
