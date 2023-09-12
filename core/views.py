from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout as authlogout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView,CreateView,DeleteView
from django.views.generic.list import ListView
from django.views import View
from django.urls import reverse_lazy
from .forms import CreateShopForm, UpdateShopForm, ChangePassword, Checkout, LoginForm, CreateProductForm, SignupCustomer, SignupShop,CouponCreateForm,CouponUpdateForm,ProductUpdateForm
from .models import Product, Brand, Price_Filter,Color, Order, Size, OrderItem, ProductStatus, Coupon
User = get_user_model()

def home(request):
    return render(request, 'home.html')


def signupcustomer(request):
    form = SignupCustomer()
    if request.method == "POST":
        form = SignupCustomer(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data['username']
            email = cleaned_data['email']
            password = cleaned_data['password']
            repassword = cleaned_data['repassword']
            if User.objects.filter(username=username).exists():
                messages.error(request, "This username already exist")
                return redirect('signupcustomer')
            if User.objects.filter(email=email).exists():
                messages.error(request, "This email already exist")
                return redirect('signupcustomer')
            if (password == repassword):
                user_obj = User.objects.create_user(username, email, password)
                user_obj.set_password(password)
                user_obj.role = 'customer'
                user_obj.save()
                messages.success(request, "Signed-up as customer successfully")
                return redirect('loginpage')
            messages.error(request, "both passwords do not match")
            return redirect('signupcustomer')
        for field_name, error_messages in form.errors.items():
            for error_message in error_messages:
                messages.error(request, f"{field_name}: {error_message}")
    return render(request, 'signup_customer.html', {'form': form})


def signupshop(request):
    form = SignupShop()
    if request.method == "POST":
        form = SignupShop(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data['username']
            email = cleaned_data['email']
            password = cleaned_data['password']
            repassword = cleaned_data['repassword']
            shopname = cleaned_data['shopname']
            address = cleaned_data['address']
            contactnumber = cleaned_data['contactnum']
            if User.objects.filter(username=username).exists():
                messages.error(request, "This username already exist")
                return redirect('signupshop')
            if User.objects.filter(email=email).exists():
                messages.error(request, "This email already exist")
                return redirect('signupshop')
            if len(contactnumber) < 10 or len(contactnumber) > 10:
                messages.error(
                    request, "contact number can not be greater or smaller then 10 digits")
                return redirect('signupshop')
            if not contactnumber.isdigit():
                messages.error(request, "contact number should be numeric")
                return redirect('signupshop')
            if (password == repassword):
                user_obj = User.objects.create_user(username, email, password)
                user_obj.set_password(password)
                user_obj.role = 'shop'
                user_obj.shopname = shopname
                user_obj.address = address
                user_obj.contact_number = contactnumber
                user_obj.save()
                messages.success(request, "Signed-up as shop successfully")
                return redirect('loginpage')
            messages.error(request, "both passwords do not match")
            return redirect('signupshop')
        for field_name, error_messages in form.errors.items():
            for error_message in error_messages:
                messages.error(request, f"{field_name}: {error_message}")
    return render(request, 'signup_shop.html', {'form': form})


def loginpage(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            login_username = cleaned_data['loginusername']
            login_password = cleaned_data['loginpassword']
            user = authenticate(
                request, username=login_username, password=login_password)
            if user is not None:
                login(request, user)
                if user.role == 'admin':
                    return redirect('admin')
                if user.role == 'customer':
                    return redirect('home')
                if user.role == 'shop':
                    return redirect('shop')
                messages.success(request, "Successfully Logged In")
            else:
                messages.error(
                    request, "Invalid credentials! Please try again")
        else:
            for field_name, error_messages in form.errors.items():
                for error_message in error_messages:
                    messages.error(request, f"{field_name}: {error_message}")
    return render(request, 'login.html', {'form': form})


@login_required(login_url="/core/loginpage/")
def logout(request):
    authlogout(request)
    messages.success(request, "Successfully logged out")
    return redirect('loginpage')


@login_required(login_url="/core/loginpage/")
def changepass(request):
    form = ChangePassword()
    if request.method == "POST":
        form = ChangePassword(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            oldpass = cleaned_data['oldpass']
            newpass = cleaned_data['newpass']
            confirmpass = cleaned_data['confirmpass']
            user_id = User.objects.get(id=request.user.id)
            check = user_id.check_password(oldpass)
            if newpass != confirmpass:
                messages.error(
                    request, 'new password and confirm password did not match')
            else:
                if check is True:
                    user_id.set_password(newpass)
                    user_id.save()
                    messages.success(
                        request, 'password changed successfully now you can login with new password')
                    return redirect('loginpage')
                messages.error(request, "your old password did not match")
        else:
            for field_name, error_messages in form.errors.items():
                for error_message in error_messages:
                    messages.error(request, f"{field_name}: {error_message}")
    return render(request, 'changepass.html', {'form': form})


class CreateShopView(CreateView):
    template_name = 'admin.html'
    form_class = CreateShopForm
    success_url = reverse_lazy('admin')  # Replace with your actual URL pattern name

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        username = cleaned_data['username']
        email = cleaned_data['email']
        password = cleaned_data['password']
        repassword = cleaned_data['repassword']
        shopname = cleaned_data['shopname']
        address = cleaned_data['address']
        contactnumber = cleaned_data['contact_number']

        if User.objects.filter(username=username).exists():
            messages.error(self.request, "This username already exists")
            return redirect('admin')

        if User.objects.filter(email=email).exists():
            messages.error(self.request, "This email already exists")
            return redirect('admin')

        if len(contactnumber) != 10 or not contactnumber.isdigit():
            messages.error(self.request, "Contact number should be 10-digit numeric")
            return redirect('admin')

        if password == repassword:
            user_obj = User.objects.create_user(username, email, password)
            user_obj.role = 'shop'
            user_obj.shopname = shopname
            user_obj.address = address
            user_obj.contact_number = contactnumber
            user_obj.save()
            messages.success(self.request, "Shop Created Successfully")
            return redirect('admin')
        else:
            messages.error(self.request, "Both passwords do not match")

        return super().form_valid(form)

    def form_invalid(self, form):
        for field_name, error_messages in form.errors.items():
            for error_message in error_messages:
                messages.error(self.request, f"{field_name}: {error_message}")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shopdetail = User.objects.filter(role='shop')
        context['shopdetail'] = shopdetail
        return context


class ShopUpdateView(UpdateView):
    model = User
    form_class = UpdateShopForm
    template_name = 'admin.html'  # Update with your template path
    success_url = reverse_lazy('admin')  # Replace with your success URL

    def form_invalid(self, form):
        response = super().form_invalid(form)
        errors = form.errors.get_json_data()
        return JsonResponse({'errors': errors}, status=400)

    def form_valid(self, form):
        response = super().form_valid(form)
        return JsonResponse({'success': 'Coupon updated successfully'})
    


class ShopDeleteView(DeleteView):
    model = User
    template_name = 'admin.html'
    success_url = reverse_lazy('admin')  # Redirect to coupon list page after successful deletion




class CreateProductView(CreateView):
    model = Product
    form_class = CreateProductForm
    template_name = 'shops.html'
    success_url = reverse_lazy('shop')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        name = cleaned_data['name']
        desc = cleaned_data['desc']
        price = cleaned_data['price']
        quantity = cleaned_data['quantity']

        errors = {}

        if name.isdigit():
            errors['name'] = ["Name is invalid"]

        if desc.isdigit():
            errors['desc'] = ["Description is invalid"]

        if not price.isdigit() or int(price) <= 0:
            errors['price'] = ["Price must be a positive number."]

        if not quantity.isdigit() or int(quantity) <= 0:
            errors['quantity'] = ["Quantity must be a positive integer."]

        if errors:
            return JsonResponse({'errors': errors})

        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shopdata = Product.objects.filter(user=self.request.user).order_by('id')
        context['shopdata'] = shopdata
        return context


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'shops.html'  # Update with your template path
    success_url = reverse_lazy('shop')  # Replace with your success URL


    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        name = cleaned_data['name']
        desc = cleaned_data['desc']
        price = cleaned_data['price']
        quantity = cleaned_data['quantity']
        
        errors = {}

        if name.isdigit():
            errors['name'] = ["Name is invalid"]

        if desc.isdigit():
            errors['desc'] = ["Description is invalid"]

        if not price.isdigit() or int(price) <= 0:
            errors['price'] = ["Price must be a positive number."]

        if not quantity.isdigit() or int(quantity) <= 0:
            errors['quantity'] = ["Quantity must be a positive integer."]

      
        if errors:
            return JsonResponse({'errors': errors})
        response = super().form_valid(form)
        return JsonResponse({'success': 'Coupon updated successfully'})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()  # Include the form in the context
        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'shops.html'
    success_url = reverse_lazy('shop')  # Redirect to coupon list page after successful deletion



@login_required(login_url="/core/loginpage/")
def customer(request):
    return render(request, 'customer.html')


def product(request):

    data = Product.objects.all()
    size = Size.objects.all()
    brand = Brand.objects.all()
    price_filter = Price_Filter.objects.all()
    color=Color.objects.all()
    catid = request.GET.get('catagories')
  
    if catid:
        data = data.filter(catagory=catid)
    else:
        data = Product.objects.all()
    page = Paginator(data, 2)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    params = {'page': page, 'catid': catid, 'brand': brand,
              'price_filter': price_filter, 'sizes': size,'color':color
              }
    return render(request, 'product.html', params)


def filter_product(request):

    data = Product.objects.all()
    catid = request.GET.get('catagories')
    brandid = request.GET.getlist('brand')
    price_filter_id = request.GET.getlist('price')
    sizeid = request.GET.getlist('size')
    colorid=request.GET.getlist('color')

# Apply filters based on the selected values
        
    data=Product.objects.filter(catagory = catid)
    if brandid: 
        data = data.filter(brand__id__in=brandid)
    elif price_filter_id:
        data = data.filter(price_filter__id__in=price_filter_id)
    elif sizeid:
        data = data.filter(size__id__in=sizeid)
    elif colorid:
        data = data.filter(color__id__in=colorid)
    else:
        data = Product.objects.all()

    page = Paginator(data, 2)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    params = {'page': page, 'filtered_data': page.object_list}
    return render(request, 'filter_product.html', params)



class FullPageView(View):
    template_name = "full-page.html"
    size_queryset = Size.objects.all()

    def get(self, request, *args, **kwargs):
        prod_id = kwargs['prod_id']
        product = Product.objects.filter(id=prod_id)
        quantity = int(Product.objects.get(id=prod_id).quantity)
        size = Size.objects.all()
        return render(request, self.template_name, {'product': product,'size': size, 'quantity': quantity})

    def post(self, request, *args, **kwargs):
        size = request.POST.get('size')
        product_id = kwargs['prod_id']
        cart = request.session.get('cart', {})

        if cart.get(product_id):
            cart[product_id] += 1
        else:
            cart[product_id] = 1

        request.session['cart'] = cart
        return redirect('cart')  # Redirect to the cart or another appropriate page



def cart(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    ids = list(request.session.get('cart').keys())
    products = Product.get_products_by_id(ids)
    total_cart_price_after_discount = 0
    total_cart_price_before_discount = 0
    coupon_discount = 0
    coupon_total_discount = 0
    if request.method == "POST":
        productid = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        quantity = cart.get(productid)
        if productid in cart:
            if remove:
                if quantity <= 1:
                    del cart[productid]
                else:
                    cart[productid] = quantity-1
            else:
                cart[productid] = quantity+1
        request.session['cart'] = cart

# Coupon logic...............
        for product in products:
            if product.id not in cart:
                quantity = cart.get(str(product.id), 0)
            else:
                quantity = cart[str(product.id)]
            total_cart_price_before_discount += product.discounted_price() * quantity
        coupon_code = request.POST.get('coupon')
        coupon = request.session.get('coupon')
        if coupon_code:
            coupon_obj = Coupon.objects.filter(
                coupon_code__iexact=coupon_code).first()
            if not coupon_obj:
                messages.error(request, "Invalid Coupon.")
                total_cart_price_after_discount = total_cart_price_before_discount
            elif coupon_obj.is_expired:
                messages.error(request, "Coupon expired.")
                total_cart_price_after_discount = total_cart_price_before_discount
           
            else:
                minimum_amount = 0
                total_after_discount = 0
                total_not_discount = 0
                coupon_applied = False
               
                for product in products:
                    quantity = cart[str(product.id)]
                    if product.user == coupon_obj.user:
                        minimum_amount = coupon_obj.minimum_amount
                        if product.discounted_price() >= minimum_amount:
                            coupon_discount = coupon_obj.discount_price
                            coupon_total_discount += coupon_discount * quantity
                            total_after_discount += (product.discounted_price()
                                                     * quantity) - coupon_total_discount
                            coupon_applied=True
                            
                        elif product.discounted_price() < minimum_amount:
                            total_not_discount += product.discounted_price() * quantity
                    else:
                        total_not_discount += product.discounted_price() * quantity
                if coupon_applied is True:
                    request.session['coupon'] = coupon_code
                    messages.success(request, f"{coupon_code} Coupon applied.")
                    
                else:
                    messages.success(request, f"{coupon_code} coupon is not valid.")
                   
                total_cart_price_after_discount = total_after_discount + total_not_discount
        else:
            total_cart_price_after_discount = total_cart_price_before_discount
    else:
        for product in products:
            quantity = cart[str(product.id)]
            total_cart_price_before_discount += product.discounted_price() * quantity
    total_cart_price_after_discount = total_cart_price_before_discount - coupon_total_discount

    return render(request, 'cart.html', {'products': products, 'total_cart_price_after_discount': total_cart_price_after_discount,
    'coupon_discount': coupon_discount, 'coupon_total_discount': coupon_total_discount})


@login_required(login_url="/core/loginpage/")
def checkout(request):
    form = Checkout()
    if request.method == "POST":
        form = Checkout(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            name = cleaned_data['name']
            address = cleaned_data['address']
            phone = cleaned_data['phone']
            user = request.user
            cart = request.session.get('cart')
            products = Product.get_products_by_id(list(cart.keys()))
            coupon_code = request.session.get('coupon')
            if len(phone) < 10 or len(phone) > 10:
                messages.error(
                    request, "contact number can not be greater or smaller then 10 digits")
                return redirect('checkout')
            if not phone.isdigit():
                messages.error(request, "contact number should be numeric")
                return redirect('checkout')
            total_before_discount = 0
            coupon_total_discount = 0
            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                total_before_discount += (product.discounted_price()
                                          ) * int(quantity)
            total_after_discount = total_before_discount
            coupon_code = request.session.get('coupon')
            if coupon_code:
                coupon_obj = Coupon.objects.filter(
                    coupon_code__iexact=coupon_code).first()
                minimum_amount = coupon_obj.minimum_amount
                if coupon_obj:
                    for product in products:
                        quantity = cart[str(product.id)]
                        if product.user == coupon_obj.user:
                            if product.discounted_price() >= minimum_amount:
                                coupon_discount = coupon_obj.discount_price
                                coupon_total_discount += coupon_discount * quantity
                        total_cart_price_after_discount = total_after_discount - coupon_total_discount
                        order = Order(user=user,
                                      name=name,
                                      address=address,
                                      phone=phone,
                                      quantity=sum(cart.values()),
                                      total=total_cart_price_after_discount,
                                      )
                    order.save()
        # product_qty=Product.objects.get(id=product.id).quantity
        # total_qty=int(product_qty) - (order.quantity)
            # print(int(product_qty))
            # print(order.quantity)
            # print(total_qty)
        # prod=Product.objects.get(id=product.id)
        # prod.quantity=total_qty
        # prod.save()
            # coupon_code = request.session.get('coupon')
            minimum_amount = 0
            coupon_total_discount = 0
            if coupon_code:
                coupon_obj = Coupon.objects.filter(
                    coupon_code__iexact=coupon_code).first()
                minimum_amount = coupon_obj.minimum_amount
                if coupon_obj:
                    for product in products:
                        price = product.discounted_price()
                        totalprice = 0
                        quantity = cart[str(product.id)]
                        if product.user == coupon_obj.user:
                            if product.discounted_price() >= minimum_amount:
                                coupon_discount = coupon_obj.discount_price
                                coupon_total_discount = coupon_discount * quantity
                                totalprice = (product.discounted_price(
                                ) * quantity) - coupon_total_discount
                            else:
                                totalprice = product.discounted_price() * quantity
                                coupon_total_discount = 0
                        else:
                            a = (product.discounted_price())
                            quantity = cart.get(str(product.id))
                            b = int(quantity)
                            totalprice = a * b
                            coupon_total_discount = 0
                        orderitem = OrderItem(
                            user=user,
                            order=order,
                            product=product,
                            price=price,
                            image=product.img,
                            quantity=cart.get(str(product.id)),
                            discount=coupon_total_discount,
                            total=totalprice,
                        )
                        orderitem.save()
                request.session['cart'] = None
                del request.session['coupon']
                return redirect('cart')

            total_cart_price_after_discount = 0
            for product in products:
                a = product.discounted_price()
                quantity = cart.get(str(product.id))
                b = int(quantity)
                totalprice = a * b
                total_cart_price_after_discount += totalprice
            order = Order(user=user,
                          name=name,
                          address=address,
                          phone=phone,
                          quantity=sum(cart.values()),
                          total=total_cart_price_after_discount,
                          )
            order.save()

            for product in products:
                a = product.discounted_price()
                quantity = cart.get(str(product.id))
                b = int(quantity)
                totalprice = a * b
                orderitem = OrderItem(
                    user=user,
                    order=order,
                    product=product,
                    price=a,
                    image=product.img,
                    quantity=cart.get(str(product.id)),
                    discount=coupon_total_discount,
                    total=totalprice,
                )
                orderitem.save()
            request.session['cart'] = None
            return redirect('cart')

        for field_name, error_messages in form.errors.items():
            for error_message in error_messages:
                messages.error(request, f"{field_name}: {error_message}")
                return redirect('checkout')
    return render(request, 'checkout.html', {'form': form})



class MyOrderListView(ListView):
    model = Order
    template_name = "myorder.html"
    context_object_name = "order"

    def get_queryset(self):
        user = self.request.user.id
        return Order.get_orders_by_user(user).order_by('id')



class OrderDetailView(ListView):
    template_name = "orderdetail.html"
    context_object_name = "orderitem"

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return OrderItem.objects.filter(order=order_id)


class CustomerOrderListView(ListView):
    template_name = "customer_orders.html"
    context_object_name = "customer_orders"
    queryset = OrderItem.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.id
        products = Product.objects.filter(user=user)
        customer_orders = context["customer_orders"].filter(product__in=products)
        status = ProductStatus.objects.all()
        context["customer_orders"] = customer_orders
        context["status"] = status
        return context



class OrderItemUpdateView(UpdateView):
    model = OrderItem
    template_name = 'customer_orders.html' 
    fields = ['status']  
    success_url = reverse_lazy('customer_order') 

    def form_valid(self, form):
        status_id = form.cleaned_data['status'].id
        status = ProductStatus.objects.get(id=status_id)
        self.object.status = status
        self.object.save()

        return super().form_valid(form)


class CouponCreateView(CreateView):
    model = Coupon
    form_class = CouponCreateForm
    template_name = 'coupon.html'
    success_url = reverse_lazy('coupon')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        errors = form.errors.get_json_data()
        return JsonResponse({'errors': errors})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        coupon_data = Coupon.objects.filter(user=self.request.user).order_by('id')
        context['coupon_data'] = coupon_data
        return context


class CouponDeleteView(DeleteView):
    model = Coupon
    template_name = 'coupon.html'
    success_url = reverse_lazy('coupon')  # Redirect to coupon list page after successful deletion



class CouponUpdateView(UpdateView):
    model = Coupon
    form_class = CouponUpdateForm
    template_name = 'coupon.html'  # Update with your template path
    success_url = reverse_lazy('coupon')  # Replace with your success URL


    def form_valid(self, form):
        response = super().form_valid(form)
        return JsonResponse({'success': 'Coupon updated successfully'})
    
    def get_initial(self):
        # Get the existing Coupon instance
        coupon = self.get_object()
        
        # Create a dictionary with field names and their initial values
        initial_data = {
            'coupon_code': coupon.coupon_code,
            'discount_price': coupon.discount_price,
            'minimum_amount': coupon.minimum_amount,
            'is_expired': coupon.is_expired,
           
        }
        return initial_data
    




