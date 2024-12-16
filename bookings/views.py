from os import getenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import stripe
from django.conf import settings
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView



# Set up your Stripe secret key
stripe.api_key = getenv('STRIPE_SECRET_KEY')  # Add your secret key in settings

class CreateCheckoutSessionView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
             # Example amount and currency
            payment_intent = stripe.PaymentIntent.create(
            amount=5000,  # £50.00
            currency="gbp",
            payment_method_types=["card"],
            description="Medical Test Booking Payment",
            )
            return JsonResponse({"client_secret": payment_intent["client_secret"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
class CheckoutView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
             # Example amount and currency
            payment_intent = stripe.PaymentIntent.create(
            amount=5000,  # £50.00
            currency="gbp",
            payment_method_types=["card"],
            description="Medical Test Booking Payment",
            )
            return JsonResponse({"client_secret": payment_intent["client_secret"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)