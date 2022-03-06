import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64

class MpesaC2bCredential:
    consumer_key='3AbkAh7EcGmWWOFN0Z8HQ0PiTESgW4XU'
    consumer_secret='w3YjxjEvAFqkM9i2'
    api_url='https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

class MpesaAccessToken:
    r=requests.get(MpesaC2bCredential.api_url,auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key,
    MpesaC2bCredential.consumer_secret))
    mpesa_access_token=json.loads(r.text)
    validated_mpesa_access_token=mpesa_access_token['access_token']

class LipanaMpesaPassword:
    lipa_time=datetime.now().strftime('%Y%m%d%H%M%S')
    business_short_code='174379'
    passkey='bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

    data_to_encode=business_short_code+passkey+lipa_time
    online_password=base64.b64encode(data_to_encode.encode())
    decode_password=online_password.decode('utf-8')