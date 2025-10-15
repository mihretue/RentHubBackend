from .views import ListingAPIView, ListingDetailAPIView
from django.urls import path


urlpatterns = [
    path("", ListingAPIView.as_view(), name="listing-list-create"),
    path("<uuid:pk>/", ListingDetailAPIView.as_view(), name="listing-detail"),
]

