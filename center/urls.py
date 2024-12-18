from django.urls import path
from .views import CenterCreateView, CenterListView, CenterByLocationListView, CenterListLocationsView

urlpatterns = [
    path('center/get/', CenterListView.as_view(), name='center-list'),
    path('center/location/get/', CenterByLocationListView.as_view(), name='center-list'),
    path('center/create/', CenterCreateView.as_view(), name='center-create'),
    path('center/locations/get/', CenterListLocationsView.as_view(), name='center_locations'),

]
