from unicodedata import category
from django.forms import FloatField
from django.shortcuts import reverse
from django.conf import settings
from django.db import models
from django.contrib.gis.db import models


# Create your models here.
CATEGORY_CHOICES=(
    ('UP','Unprocessed'),
    ('P','Processed')
)
LABEL_CHOICES=(
    ('P','primary'),
    ('S','Processed'),
    ('D','danger')
)
VENDOR_CHOICES=(
    ('FRA','FRANCHISES'),
    ('RES','RESTAURANTS'),
    ('MON','FISHMONGERS')
)
FOOD_TYPES=(
    ('food', 'food'),
    ('accompaniments', 'accompaniments'),
    ('beverages', 'beverages'),
    ('Veggies','Veggies')
)
SIZE=(
    ('Full','full'),
    (1/4,'quarter'),
    (1/2,'half')
)

AVAILABILITY_STATUS=(
    ('Unavailable','unavailable'),
    ('Available','available')
)
HOURS_OPEN=(
    ('24 Hours','24 hours'),
    ('Till Midnight','till midnight'),
    ('Till 8pm','till 8pm')
)
BIZ_STATUS=(
    ('OP','open'),
    ('CL','closed')
)
DAYS_OF_WEEK = (
    ('Everyday', 'everyday'),
    ('Weekdays', 'weekdays'),
    ('Everyday excluding Sunday', 'everyday excluding sunday'),
    ('Everyday plus holidays', 'everyday plus holidays'),
)
RATING_CHOICES = (
    (1, 'Poor'),
    (2, 'Average'),
    (3, 'Good'),
    (4, 'Very Good'),
    (5, 'Excellent')
)
FISH_TYPES=(
    ('Fresh, Ungutted, Chilled','Fresh, Ungutted, Chilled'),
    ('Fresh, Ungutted, Frozen','Fresh, Ungutted, Frozen'),
    ('Fresh, Gutted, Chilled','Fresh, Gutted, Chilled'),
    ('Fresh, Gutted, Frozen','Fresh, Gutted, Frozen'),
    ('Processed, Fillet, Chilled','Processed, Fillet, Chilled'),
    ('Processed, Fillet, Frozen','Processed, Fillet, Frozen'),
    ('Processed, Sundried','Processed, Sundried'),
    ('Processed, Smoked','Processed, Smoked'),
    ('Processed, Fried','Processed, Fried')
)

class Item(models.Model):
    title=models.CharField(max_length=100)
    price=models.FloatField()
    discount_price=models.FloatField(blank=True,null=True)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=5)
    label=models.CharField(choices=LABEL_CHOICES,max_length=2)
    slug=models.SlugField()
    description=models.TextField()
    item_pic=models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("store:products",kwargs={
            'slug':self.slug
        })
    def get_add_to_cart_url(self):
        return reverse("store:add-to-cart",kwargs={
            'slug':self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("store:remove-from-cart",kwargs={
            'slug':self.slug
        })


class Franchise(models.Model):
    name = models.CharField(max_length=100)
    coords = models.PointField(blank=True,null=True)
    address = models.CharField(max_length=100,blank=True,null=True)
    location = models.CharField(max_length=50)
    open_status=models.CharField(max_length=10,choices=BIZ_STATUS)
    days_open=models.CharField(max_length=100,choices=DAYS_OF_WEEK)
    fish_type=models.CharField(max_length=100,choices=FISH_TYPES)
    franchise_pic=models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)

    def __str__(self) -> str:
        return self.name

class Mongers(models.Model):
    name = models.CharField(max_length=50)
    location= models.CharField(max_length=80)
    phoneNumber = models.CharField(max_length=10)
    coords=models.PointField(blank=True,null=True)
    monger_pic=models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)

    def __str__(self) -> str:
        return self.name
    
class FoodItem(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    price=models.FloatField()
    discount_price=models.FloatField(blank=True,null=True)
    type = models.CharField(max_length=100, choices=FOOD_TYPES)
    available=models.CharField(max_length=50,choices=AVAILABILITY_STATUS)
    size=models.CharField(max_length=20,choices=SIZE,blank=True)
    slug=models.SlugField()
    food_pic=models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100,blank=True)

    def __str__(self) -> str:
        return self.name

    
    def get_absolute_url(self):
        return reverse("store:food-products",kwargs={
            'slug':self.slug
        })
    def get_food_add_to_cart_url(self):
        return reverse("store:food-add-to-cart",kwargs={
            'slug':self.slug
        })

    def get_food_remove_from_cart_url(self):
        return reverse("store:remove-food-from-cart",kwargs={
            'slug':self.slug
        })


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)
    location=models.CharField(max_length=100)
    coords=models.PointField(blank=True,null=True)
    phoneNumber = models.CharField(max_length=10)
    food_items=models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    open_status=models.CharField(max_length=10,choices=BIZ_STATUS)
    days_open=models.CharField(max_length=100,choices=DAYS_OF_WEEK)
    restaurant_pic=models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100,)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("store:restaurants",kwargs={
            'slug':self.slug
        })


#order items for the raw fish
class OrderItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    ordered=models.BooleanField(default=False)
    

    def __str__(self) -> str:
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity*self.item.price

    def get_total_discount_item_price(self):
        return self.quantity*self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price()-self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        
        return self.get_total_item_price()
        

#restaurant order items
class RestaurantOrderItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item=models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    ordered=models.BooleanField(default=False)
    

    def __str__(self) -> str:
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return self.quantity*self.item.price

    def get_total_discount_item_price(self):
        return self.quantity*self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price()-self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        
        return self.get_total_item_price()      

class BillingAddress(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=100)
    email=models.EmailField()
    location=models.CharField(max_length=100)
    delivery_address=models.CharField(max_length=100)
    

    def __str__(self):
        return self.user.username 

class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)
    billing_address=models.ForeignKey('BillingAddress',on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self) -> str:
        return self.user.username

    def get_total(self):
        total=0
        for order_item in self.items.all():
            total += order_item.get_final_price()

        return total

class RestaurantOrder(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items=models.ManyToManyField(RestaurantOrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)
    billing_address=models.ForeignKey(BillingAddress,on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self) -> str:
        return self.user.username

    def get_total(self):
        total=0
        for order_item in self.items.all():
            total += order_item.get_final_price()

        return total



    # def __str__(self):
    #     return "%s the place" % self.name




class Payment(models.Model):
    mpesa_charge_id=models.CharField(max_length=50)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True)
    amount=models.FloatField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Reservation(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    reserveDate=models.DateField()
    phoneNumber=models.CharField(max_length=100)
    reserveTime=models.DateTimeField()
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE,blank=True)
    familySize=models.IntegerField()
    reserveOrder=models.TextField()

    def __str__(self):
        return self.user.username
