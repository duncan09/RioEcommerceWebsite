from django.urls import reverse
from urllib import request
from django.shortcuts import redirect, render,get_object_or_404
from django.template import context
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView,DetailView,TemplateView,View

# from store.mpesa_credentials import LipanaMpesaPassword, MpesaAccessToken
from store.models import FoodItem, Franchise, Item, Mongers,OrderItem,Order,Franchise, Reservation,Restaurant,BillingAddress, RestaurantOrder, RestaurantOrderItem
from django.utils import timezone
from django.contrib import messages
from django.views import generic
from django.contrib.gis.geos import fromstr,Point
from django.contrib.gis.db.models.functions import Distance
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm, ReservationForm
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth
import json
from django_daraja.mpesa.core import MpesaClient
# Create your views here.

 	
latitude=-1.2582438
longitude=36.7064952
user_location=Point(longitude,latitude,srid=4326)

class VendorView(generic.ListView):
    model=Franchise
    context_object_name = 'vendors'
    queryset = Franchise.objects.all()   #annotate(distance=Distance('location',
    # user_location)
    # ).order_by('distance')[0:6]
    template_name = 'vendor.html'
    

    # def get_paginate_by(self, queryset):
    #     """
    #     Try to fetch pagination by user settings,
    #     If there is none fallback to the original.
    #     """

    #     try:
    #         self.paginate_by = self.user_settings.objects.get(user=self.request.user.id).per_page
    #     except:
    #         pass
    #     return self.paginate_by

# a class to show all the fishmongers
class MongerView(generic.ListView):
    model=Mongers
    context_object_name = 'mongers' 
    template_name = 'mongers.html'

#this is a class to render the home page instead of creating a function for it
class HomeView(ListView):
    model=Item
    template_name="home-page.html"

def about_page(request):
    
    return render(request,"about.html")

class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            order=Order.objects.get(user=self.request.user,ordered=False)
            context={'object':order,}
            return render(self.request,"order_summary.html",context)
        except ObjectDoesNotExist:
            messages.error(request,"You do not have an active order")
            return redirect("/")

#create an order summary for the food items
class FoodOrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            order=RestaurantOrder.objects.get(user=self.request.user,ordered=False)
            context={'object':order,}
            return render(self.request,"food_order_summary.html",context)
        except ObjectDoesNotExist:
            messages.error(request,"You do not have an active order")
            return redirect("/")


class CheckoutView(View):
    def get(self,*args,**kwargs):
        form=CheckoutForm()
        context={
            'form':form
        }
        return render(self.request,"checkout-page.html",context)

    def post(self,*args,**kwargs):
        form=CheckoutForm(self.request.POST or None)
        try:
            order=Order.objects.get(user=self.request.user,ordered=False)
            if form.is_valid():
            
                first_name=form.cleaned_data.get('first_name')
                last_name=form.cleaned_data.get('last_name')
                phone_number=form.cleaned_data.get('phone_number')
                email=form.cleaned_data.get('email')
                location=form.cleaned_data.get('location')
                delivery_address=form.cleaned_data.get('delivery_address')
                # same_billing_address=form.cleaned_data.get('same_billing_address')
                # save_info=form.cleaned_data.get('save_info')
                billing_address=BillingAddress(
                user=self.request.user,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                email=email,
                location=location,
                delivery_address=delivery_address,
                # same_billing_address=same_billing_address,
                # save_info=save_info
                )
                messages.info(self.request,"Your details have been received")
                billing_address.save()
                order.billing_address=billing_address
                order.save()
                #TODO: redirect to the payment option
                
                return redirect('store:checkout')
            messages.warning(self.request,"Failed checkout")
            return redirect('store:checkout')

            
        except ObjectDoesNotExist:
            messages.error(request,"You do not have an active order")
            return redirect("store:order-summary")

#a function for the restaurant check out page
class RestaurantCheckoutView(View):
    def get(self,*args,**kwargs):
        form=CheckoutForm()
        context={
            'form':form
        }
        return render(self.request,"checkoutRestaurant.html",context)

    def post(self,*args,**kwargs):
        form=CheckoutForm(self.request.POST or None)
        try:
            order=RestaurantOrder.objects.get(user=self.request.user,ordered=False)
            if form.is_valid():
            
                first_name=form.cleaned_data.get('first_name')
                last_name=form.cleaned_data.get('last_name')
                phone_number=form.cleaned_data.get('phone_number')
                email=form.cleaned_data.get('email')
                location=form.cleaned_data.get('location')
                delivery_address=form.cleaned_data.get('delivery_address')
                # same_billing_address=form.cleaned_data.get('same_billing_address')
                # save_info=form.cleaned_data.get('save_info')
                billing_address=BillingAddress(
                user=self.request.user,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                email=email,
                location=location,
                delivery_address=delivery_address,
                # same_billing_address=same_billing_address,
                # save_info=save_info
                )
                messages.info(self.request,"Your details have been received")
                billing_address.save()
                order.billing_address=billing_address
                order.save()
                #TODO: redirect to the payment option
                
                return redirect('store:restaurant-checkout')
            messages.warning(self.request,"Failed checkout")
            return redirect('store:restaurant-checkout')

            
        except ObjectDoesNotExist:
            messages.error(request,"You do not have an active order")
            return redirect("store:food-order-summary")
        
        
class PaymentView(View):
    def get(self,*args,**kwargs):
        return render(self.request,'payment.html')
        

class TestView(ListView):
    model=Item
    template_name="test_product.html"


# def checkout_page(request):
#     context={
#         'items':Item.objects.all
#     }
#     return render(request,"checkout-page.html",context)


#this is a class to display the products in the product details page
class ItemDetailView(DetailView):
    model=Item
    template_name="product-page.html"

#this is to display the products in the food products page
class FoodDetailView(DetailView):
    model=FoodItem
    template_name="chosen_food_items.html"



#defining a method that will add an order to cart and remove it when removed
@login_required
def add_to_cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order_item,created=OrderItem.objects.get_or_create(item=item,user=request.user,ordered=False)
    order_qs=Order.objects.filter(user=request.user,ordered=False)#make sure its not already ordered
    if order_qs.exists():
        order=order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            return redirect("store:order-summary")
            messages.info(request,"This item was updated")

        else:
            messages.info(request,"This item was added to your cart")
            order.items.add(order_item)
            return redirect("store:order-summary")

    else:
        ordered_date=timezone.now()
        order=Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)

    return redirect("store:order-summary")


#defining a method that will add a restaurant order to cart and remove it when removed
@login_required
def food_add_to_cart(request,slug):
    item=get_object_or_404(FoodItem,slug=slug)
    order_item,created=RestaurantOrderItem.objects.get_or_create(item=item,user=request.user,ordered=False)
    order_qs=RestaurantOrder.objects.filter(user=request.user,ordered=False)#make sure its not already ordered
    if order_qs.exists():
        order=order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            return redirect("store:food-order-summary")
            messages.info(request,"This item was updated")

        else:
            messages.info(request,"This item was added to your cart")
            order.items.add(order_item)
            return redirect("store:food-order-summary")

    else:
        ordered_date=timezone.now()
        order=RestaurantOrder.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)

    return redirect("store:food-order-summary")

#removing order from cart
@login_required
def remove_from_cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order_qs=Order.objects.filter(user=request.user,ordered=False)

    if order_qs.exists():
        order=order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request,"This item was removed from your cart")
            return redirect("store:order-summary")
        else:
            messages.info(request,"This item is not in your cart")
            return redirect("store:products",slug=slug)
    else:
        messages.info(request,"You do not have an active order")
        return redirect("store:products",slug=slug)
    return redirect("store:products",slug=slug)


#removing food order from cart
@login_required
def food_remove_from_cart(request,slug):
    item=get_object_or_404(FoodItem,slug=slug)
    order_qs=RestaurantOrder.objects.filter(user=request.user,ordered=False)

    if order_qs.exists():
        order=order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item=RestaurantOrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request,"This item was removed from your cart")
            return redirect("store:food-order-summary")
        else:
            messages.info(request,"This item is not in your cart")
            return redirect("store:food-products",slug=slug)
    else:
        messages.info(request,"You do not have an active order")
        return redirect("store:food-products",slug=slug)
    return redirect("store:food-products",slug=slug)

@login_required
def remove_single_from_cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order_qs=Order.objects.filter(user=request.user,ordered=False)

    if order_qs.exists():
        order=order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity>1:
                order_item.quantity -=1
                order_item.save()
            else:
                order.items.remove(order_item)
            
            messages.info(request,"This item quantity was updated")
            return redirect("store:order-summary")
        else:
            messages.info(request,"This item is not in your cart")
            return redirect("store:products",slug=slug)
    else:
        messages.info(request,"You do not have an active order")
        return redirect("store:products",slug=slug)
    return redirect("store:products",slug=slug)

#removing single food item from cart
@login_required
def remove_single_fooditem_from_cart(request,slug):
    item=get_object_or_404(FoodItem,slug=slug)
    order_qs=RestaurantOrder.objects.filter(user=request.user,ordered=False)

    if order_qs.exists():
        order=order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item=RestaurantOrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity>1:
                order_item.quantity -=1
                order_item.save()
            else:
                order.items.remove(order_item)
            
            messages.info(request,"This item quantity was updated")
            return redirect("store:food-order-summary")
        else:
            messages.info(request,"This item is not in your cart")
            return redirect("store:food-products",slug=slug)
    else:
        messages.info(request,"You do not have an active order")
        return redirect("store:food-products",slug=slug)
    return redirect("store:food-products",slug=slug)

#the restaurant view
class RestaurantView(ListView):
    model = Restaurant
    template_name = 'restaurant.html'
    context_object_name="restaurants"

    # def get_context_data(self,**kwargs):
    #     context = super(Menu, self).get_context_data(**kwargs)
    #     restaurant = Restaurant.objects.get(name='McDonalds')
    #     context['restaurant'] = Restaurant.objects.get(name='McDonalds')
    #     context['menu'] = Menu.objects.get(restaurant=restaurant)
    #     return context

#the food items view
class FoodItemView(ListView):
    model = FoodItem
    template_name = 'menu_page.html'
    context_object_name="food_items"

#access token for the Mpesa integration sandbox
def getAccessToken(request):
    consumer_key='3AbkAh7EcGmWWOFN0Z8HQ0PiTESgW4XU'
    consumer_secret='w3YjxjEvAFqkM9i2'
    api_url='https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r=requests.get(api_url,auth=HTTPBasicAuth(consumer_key,consumer_secret))
    mpesa_access_token=json.laods(r.text)
    validated_mpesa_access_token=mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)

#accessing and integrating with the Mpesa payment module
# def lipa_na_mpesa_online(request):
#     access_token=MpesaAccessToken.validated_mpesa_access_token
#     api_url="https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
#     headers={"Authorization":"Bearer %s" %access_token}
#     request={
#         "BusinessShortCode":LipanaMpesaPassword.business_short_code,
#         "password":"MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjIwMjE0MTIyMzE5",
#         "Timestamp":LipanaMpesaPassword.lipa_time,
#         "TransactionType":"CustomerPayBillOnline",
#         "Amount":1,
#         "PartyA":254716176773,
#         "PartyB":LipanaMpesaPassword.business_short_code,
#         "PhoneNumber":254716176773,
#         "CallBackURL":"https://mydomain.com/path",
#         "AccountReference":"CompanyXLTD",
#         "TransactionDesc":"Payment of X"
#     }
#     response=requests.post(api_url,json=request,headers=headers)
#     return HttpResponse(response)


def test_lipa(request):
    cl=MpesaClient()
    phone_number='0716176773'
    amount=1
    account_ref='reference'
    transaction_desc='Description'
    mpesa_stk_push_callback=r'https://darajambili.herokuapp.com/express-payment'
    callback_url=request.build_absolute_uri(reverse(mpesa_stk_push_callback))
    response=cl.stk_push(phone_number,amount,account_ref,transaction_desc,callback_url)

    return HttpResponse(response)

def stk_push_callback(request):
    data=request.body
    return HttpResponse('https://darajambili.herokuapp.com/express-payment')



# not required

#creating a view for the reservation form
@login_required
def reservationForm(View):
    if request.method=='POST':
        form=ReservationForm(request.POST,user=request.user)
        if form.is_valid():
            fullName=request.cleaned_data.get()
            reserveDate=request.POST['date']
            reserveTime=request.POST['time']
            phoneNumber=request.POST['phoneNumber']
            familySize=request.POST['familySize']
            reserveOrder=request.POST['order']

    reserveOrder=Reservation.objects.create(
        fullName=fullName,
        reserveDate=reserveDate,
        reserveTime=reserveTime,
        phoneNumber=phoneNumber,
        familySize=familySize,
        reserveOrder=reserveOrder
    )
        
        
    
    