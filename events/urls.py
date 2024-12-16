from django.urls import path
from .views import GoogleCalendarCreateEventAPIView, GoogleCalendarEventsAPIView, GoogleCalendarFilteredEventsAPIView, GoogleCalendarGetFreeSlotsAPIView

urlpatterns = [
    path('calendar/events/', GoogleCalendarEventsAPIView.as_view(), name='google_calendar_events'),
    path('calendar/create-event/', GoogleCalendarCreateEventAPIView.as_view(), name='google_calendar_create_event'),
    path('calendar/filtered-events/', GoogleCalendarFilteredEventsAPIView.as_view(), name='google_calendar_filtered_events'),
    path('calendar/free-slots/', GoogleCalendarGetFreeSlotsAPIView.as_view(), name='google_calendar_get_free_slots'),
]
