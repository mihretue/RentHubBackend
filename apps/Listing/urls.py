from .views import ListingAPIView, ListingDetailAPIView, BulkListingView
from django.urls import path


urlpatterns = [
    path("", ListingAPIView.as_view(), name="listing-list-create"),
    path("bulk_upload", BulkListingView.as_view(), name="bulk-list-create"),
    path("<uuid:pk>/", ListingDetailAPIView.as_view(), name="listing-detail"),
]

