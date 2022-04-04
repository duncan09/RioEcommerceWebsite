from cProfile import label
from dataclasses import fields
from datetime import datetime
from email.utils import format_datetime
from ssl import Options
from unittest.util import _MAX_LENGTH
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from store.models import Restaurant


RESTAURANT_CHOICES=(
    ('1','The Loft'),
    ('2','Kilimanjaro')
)
class CheckoutForm(forms.Form):
    first_name=forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'duncan'
    }))
    last_name=forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'mugambi'
    }))
    phone_number=forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'0720123123'
    }))
    email=forms.CharField(required=False,widget=forms.TextInput(attrs={
        'placeholder':'name@example.com'
    }))
    location=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Kisii town'}))
    delivery_address=forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'Bel apartments,Hse No.3, opapo'}))
    same_billing_address=forms.BooleanField(required=False,widget=forms.CheckboxInput())
    save_info=forms.BooleanField(required=False,widget=forms.CheckboxInput())


class ReservationForm(forms.Form):
    fullName=forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'duncan'
    }))
    reserveDate=forms.DateField()
    reserveTime=forms.TimeField()
    restaurant=forms.ModelChoiceField(queryset=Restaurant.objects.all())
    phoneNumber=forms.CharField()
    familySize=forms.IntegerField()
    reserveOrder=forms.CharField(widget=forms.Textarea)

class UserSignUpForm(UserCreationForm):
    mobile=forms.CharField(max_length=11)
    fullName=forms.CharField(max_length=100)
    class Meta:
        model=User
        fields=('fullName','username','mobile','password1','password2')
        labels={'fullname':'Full Name','mobile':'Mobile Number'}