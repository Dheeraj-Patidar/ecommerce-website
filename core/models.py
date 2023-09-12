import datetime
from django.db import models
from django.contrib.auth.models import User, AbstractUser

class Card(models.Model):
    titel=models.CharField(max_length=100)
    desc=models.CharField(max_length=500)
    # image=models.FileField(upload_to="images", default=None)
    def __str__(self):
        return str(self.titel)


class User(AbstractUser):
    role=(
    ('admin','ADMIN'),
    ('shop','SHOP'),
    ('customer','CUSTOMER')
)
    username=models.CharField(max_length=100, unique=True)
    email=models.EmailField(max_length=100, unique=True)
    shopname=models.CharField(max_length=100, default=None, null=True)
    address=models.CharField(max_length=100, default=None, null=True)
    contact_number=models.CharField(max_length=10, default=None, null=True)
    role=models.CharField(max_length=50, choices=role, default='admin')
    USERNAME_FIELD='username'
    # REQUIRED_FIELDS=['email']

    def __str__(self):
        return str(self.username)



class Catagory(models.Model):
    catagory=(
        ('men','MENS'),
        ('women','WOMEN'),
        ('kid','KID'),
        ('homeliving','HOMELIVING'),
        ('beauty','BEAUTY')
    )

    catagory=models.CharField(max_length=50, choices=catagory,default=None,null=True)
    name=models.CharField(max_length=200,default=None,null=True) 

    objects = models.Manager() 
    def __str__(self):
        return '%s , %s '%(self.name , self.catagory)


class Brand(models.Model):
    name=models.CharField(max_length=150,default=None,null=True)

    objects = models.Manager() 
    def __str__(self):
        return str(self.name)

class Price_Filter(models.Model):
    price=(
        ('124 to 2743','124 TO 2743'),
        ('2743 to 5362','2743 TO 5362'),
        (' 5362 to 7981',' 5362 TO 7981'),
        (' 7981 to 10600',' 7981 TO 10600')
    
    )
    price=models.CharField(max_length=150, choices=price,default=None,null=True)

    objects = models.Manager() 
    def __str__(self):
        return self.price

class Color(models.Model):

    color = (
        ('black','BLACK'),
        ('blue', 'BLUE'),
        ('white','WHITE'),
        ('green', 'GREEN'),
        ('red', 'RED'),
        ('grey','GREY')
        # Add more color choices as needed
    )
    color=models.CharField(max_length=150, choices=color,default=None,null=True)

    objects = models.Manager()
    def __str__(self):
        return self.color

class Size(models.Model):
    size=models.CharField(max_length=10,default=None,null=True)

    objects = models.Manager() 
    def __str__(self):
        return str(self.size)
    
class ProductStatus(models.Model):
    status_choices=(
        ('pending','PENDING'),
        ('dispatch','DISPATCH'),
        ('on the way','ON THE WAY'),
        ('delivered','DELIVERED'),
        ('cancel','CANCEL'),
        ('return','RETURN')
    )
    status=models.CharField(max_length=150, choices=status_choices,default=None,null=True)
    objects = models.Manager() 
    def __str__(self):
        return str(self.status)

class FestivalDiscount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None, null=True)
    discount_percentage = models.IntegerField(null=True,default=10)
    start_date = models.DateField(default=datetime.datetime.today)
    end_date = models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return f"{self.user} - {self.discount_percentage}% Festival Discount"

class Coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None, null=True)
    coupon_code=models.CharField(max_length=10,default=None,null=True)
    is_expired=models.BooleanField(default=False)
    discount_price=models.IntegerField(default=None,null=True)
    minimum_amount=models.IntegerField(default=None,null=True)
    
    objects = models.Manager() 
    def __str__(self):
        return str(self.coupon_code)

class Product(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    catagory=models.ForeignKey(Catagory, on_delete=models.CASCADE, default=None, null=True)
    name=models.CharField(max_length=100,default=None,null=True,blank=True)
    desc=models.CharField(max_length=200,default=None,null=True)
    price=models.CharField(max_length=20,default=None)
    quantity=models.CharField(max_length=1000,default=0,blank=True)
    img=models.FileField(upload_to='images',default=None)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,default=None,null=True)
    price_filter=models.ForeignKey(Price_Filter,on_delete=models.CASCADE,default=None,null=True)
    color=models.ForeignKey(Color,on_delete=models.CASCADE,default=None,null=True)
    size=models.ForeignKey(Size,on_delete=models.CASCADE,default=None,null=True)
    discount=models.IntegerField(default=10,null=True)
    objects = models.Manager() 

    def discounted_price(self):
        discount_amount = float(self.discount / 100) * float(self.price)
        return int(self.price) - int(discount_amount)

    # def get_discounted_price(self, festival_discount):
    #     if self.user == festival_discount.user:
    #         discount_percentage = festival_discount.discount_percentage
    #         discounted_amount = self.price * int(discount_percentage / 100)
    #         discounted_price = self.price - discounted_amount
    #         return discounted_price
    #     return self.price 
    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in = ids)

    def __str__(self):
        return str(self.name)


class Order(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None,null=True)
    name=models.CharField(max_length=100,default=None,null=True)
    address=models.CharField(max_length=100,default=None,null=True)
    phone=models.CharField(max_length=50,default=None,null=True)
    date=models.DateField(default=datetime.datetime.today)
    quantity=models.IntegerField(default=None,null=True)
    total=models.CharField(max_length=100,default=None,null=True)
    status=models.BooleanField(default=False)
    
    @staticmethod
    def get_orders_by_user(user_id):
        return Order.objects.filter(user = user_id)

    objects = models.Manager() 
    def __str__(self):
        return str(self.name)

class OrderItem(models.Model):
    status=models.ForeignKey(ProductStatus,on_delete=models.CASCADE,default="1",null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None,null=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,default=None,null=True)
    image=models.FileField(upload_to='images',default=None)
    date=models.DateField(default=datetime.datetime.today)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField(default=None,null=True)
    discount=models.IntegerField(default=0,null=True)
    total=models.CharField(max_length=1000,default=None,null=True)

    objects = models.Manager() 

    def __str__(self):
        return str(self.order)

