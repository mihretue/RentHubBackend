from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django_rest_passwordreset.views import ResetPasswordRequestToken, ResetPasswordConfirm

# --- Helper function to safely apply swagger_auto_schema ---
def safe_swagger_auto_schema(view_method, **kwargs):
    """Apply swagger_auto_schema safely even if previously applied"""
    if hasattr(view_method, "_swagger_auto_schema"):
        delattr(view_method, "_swagger_auto_schema")
    return swagger_auto_schema(**kwargs)(view_method)


# --- Swagger schema config ---
schema_view = get_schema_view(
    openapi.Info(
        title="RentHub API",
        default_version='v1',
        description="API documentation for RentHub backend",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@renthub.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

ResetPasswordRequestToken.post = safe_swagger_auto_schema(
    ResetPasswordRequestToken.post,
    operation_description="Send password reset link to email",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
        },
        required=['email'],
    ),
    responses={200: 'Reset link sent if email exists.'},
)

ResetPasswordConfirm.post = safe_swagger_auto_schema(
    ResetPasswordConfirm.post,
    operation_description="Confirm password reset with token",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['token', 'password'],
    ),
    responses={200: 'Password reset successful.'},
)

# --- URLs ---
urlpatterns = [
    path('admin/', admin.site.urls),

    # App endpoints
    path('api/users/', include("apps.Users.urls")),
    path('api/listings/', include("apps.Listing.urls")),
    path('api/bookings/', include("apps.Bookings.urls")),
    path('api/payments/', include("apps.Bookings.urls")),
    path('api/payments/note/', include("apps.Bookings.urls")),

    # Swagger & ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
