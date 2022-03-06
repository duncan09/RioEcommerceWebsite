from django import forms

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
    fullName=forms.CharField()
    reserveDate=forms.DateField()
    reserveTime=forms.DateTimeField()
    phoneNumber=forms.CharField()
    familySize=forms.IntegerField()
    reserveOrder=forms.CharField(max_length=400)

    def __str__(self):
        return self.name
