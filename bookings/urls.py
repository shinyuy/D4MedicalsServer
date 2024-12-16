from django.urls import path
from .views import CreateCheckoutSessionView

urlpatterns = [
    path('booking/create-payment-intent/', CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
    path('booking/driver-details/', CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
]