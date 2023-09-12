# from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import CouponUpdateView,CouponCreateView,CouponDeleteView,CreateProductView,ProductDeleteView,ProductUpdateView,ShopUpdateView,OrderItemUpdateView,CreateShopView,ShopDeleteView,CustomerOrderListView,OrderDetailView,MyOrderListView,FullPageView

urlpatterns=[
   path('',views.home,name='home'),
   path('signupcustomer/',views.signupcustomer,name='signupcustomer'),
   path('signupshop/',views.signupshop,name='signupshop'),
   path('loginpage/',views.loginpage,name='loginpage'),
   path('home/',views.home,name='home'),
   path('logout/',views.logout,name='logout'),
   path('changepass/',views.changepass,name='changepass'),
   path('reset_password/',auth_views.PasswordResetView.as_view(template_name="reset_password.html"), name="reset_password"),
   path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"),name="password_reset_done"),
   path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="reset_password_form.html") ,name="password_reset_confirm"),
   path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_done.html"),name="password_reset_complete"),
   path('admin/',CreateShopView.as_view(),name='admin'),
   path('shop/',CreateProductView.as_view(),name='shop'),
   path('updateproduct/<int:pk>/',ProductUpdateView.as_view(), name='updateproduct'),
   path('deleteproduct/<int:pk>/',ProductDeleteView.as_view(),name='deleteproduct'),
   path('customer/',views.customer,name='customer'),
   path('product/',views.product,name='product'),
   path('filter_product/',views.filter_product,name='filter_product'),
   path('fullpage/<int:prod_id>',FullPageView.as_view(),name='fullpage'),
   path('updateshop/<int:pk>/', ShopUpdateView.as_view(), name='updateshop'),
   path('deleteshop/<int:pk>/',ShopDeleteView.as_view(),name='deleteshop'),
   path('cart/',views.cart,name='cart'),
   path('checkout/',views.checkout,name='checkout'),
   path('myorder/',MyOrderListView.as_view(),name='myorder'),
   path('orderdetail/<int:order_id>/',OrderDetailView.as_view(),name='orderdetail'),
   path('customer_order/',CustomerOrderListView.as_view(),name='customer_order'),
   path('updatestatus/<int:pk>/',OrderItemUpdateView.as_view(),name='updatestatus'),
   path('coupon/', CouponCreateView.as_view(), name='coupon'),
   path('deletecoupon/<int:pk>/',CouponDeleteView.as_view(),name='deletecoupon'),
   path('updatecoupon/<int:pk>/', CouponUpdateView.as_view(), name='updatecoupon'),
   
  ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)