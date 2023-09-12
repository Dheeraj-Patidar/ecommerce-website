from django.contrib import admin

from .models import Card,User,Product,Catagory,Brand,Price_Filter,Color,Order,Size,OrderItem,ProductStatus,FestivalDiscount,Coupon
admin.site.register(Card)
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Catagory)
admin.site.register(Brand)
admin.site.register(Price_Filter)
admin.site.register(Order)
admin.site.register(Size)
admin.site.register(OrderItem)
admin.site.register(ProductStatus)
admin.site.register(FestivalDiscount)
admin.site.register(Coupon)
admin.site.register(Color)
