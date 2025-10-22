from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, PaymentViewSet, PaymentNoteViewSet

router = DefaultRouter()
router.register("bookings", BookingViewSet, basename="booking")
router.register("payments", PaymentViewSet, basename="payment")
router.register("notes", PaymentNoteViewSet, basename="paymentnote")

urlpatterns = router.urls
