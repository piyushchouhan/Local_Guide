from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from localguides.models import Booking, Guide
import requests
import json
from paytmchecksum import PaytmChecksum

@login_required 
def payment_view(request, booking_id):
    # Retrieve the booking object based on the booking_id
    booking = get_object_or_404(Booking, pk=booking_id)
    guide = get_object_or_404(Guide, pk=booking.guide_id)
    rate = guide.rate_per_hour
    paytm_params = dict()
     # Construct Paytm QR code generation request
    paytm_params["body"] = { 
            "mid": "YOUR_MID_HERE",
            "orderId": f"ORDERID_{booking.id}",  # Use a unique identifier for each booking
            "amount": str(rate),  # Replace with the actual amount
            "businessType": "UPI_QR_CODE",
            "posId": "S12_123",
    }

    # Generate checksum for the request
    checksum = PaytmChecksum.generateSignature(json.dumps(paytm_params["body"]), "12345678901234567890123456789012")

    # Add checksum to the request
    paytm_params["head"] = {
        "clientId": "C11",
        "version": "v1",
        "signature": checksum
    }
    

    # Make the request to Paytm API
    url = "https://securegw-stage.paytm.in/paymentservices/qr/create"
    response = requests.post(url, data=json.dumps(paytm_params), headers={"Content-type": "application/json"}).json()
    try:
        qr_code_data = response['body']
    except KeyError:
    # Handle the case where 'body' key is not present in the response
        qr_code_data = None  

    # Render the payment page with booking information and Paytm QR code data
    return render(request, 'payment/payment_page.html', {'booking': booking, 'qr_code_data': qr_code_data})


