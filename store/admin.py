
from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Franchise, Item, Mongers,OrderItem,Order, Reservation, Restaurant, Franchise,FoodItem, RestaurantOrder, RestaurantOrderItem,BillingAddress
from django.contrib.gis.admin import OSMGeoAdmin
from django.utils.translation import gettext_lazy

# Register your models here.
class VendorAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')

class FranchiseAdmin(admin.ModelAdmin):
    list_display=('name','address','location')

class RestaurantAdmin(admin.ModelAdmin):
    list_display=('name','address','location','open_status')

class OrderAdmin(admin.ModelAdmin):
    list_display=('ordered','billing_address') 

class ReserveAdmin(admin.ModelAdmin):
    list_display=('username','reserveDate','reserveTime','restaurant','reserveOrder') 

class ItemAdmin(admin.ModelAdmin):
    list_display=('title','price','category','label','description')

class FoodItemAdmin(admin.ModelAdmin):
    list_display=('name','description','price','type','size')

# class MyAdminSite(AdminSite):
#     # Text to put at the end of each page's <title>.
#     site_title = gettext_lazy('Rio')

#     # Text to put in each page's <h1> (and above login form).
#     site_header = gettext_lazy('RioFish Ecommerce')

#     # Text to put at the top of the admin index page.
#     index_title = gettext_lazy('Rio Ecommerce Admin Area')

# admin.site = MyAdminSite()

admin.site.site_header = 'Rio E-commerce'                    # default: "Django Administration"
admin.site.index_title = 'Rio Admin Area'                 # default: "Site administration"
admin.site.site_title = 'Administration' # default: "Django site admin"


admin.site.register(Item,ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(RestaurantOrderItem)
admin.site.register(Order,OrderAdmin)
admin.site.register(RestaurantOrder)
admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(FoodItem,FoodItemAdmin)
admin.site.register(Franchise,FranchiseAdmin)
admin.site.register(Mongers)
admin.site.register(Reservation)
admin.site.register(BillingAddress)

