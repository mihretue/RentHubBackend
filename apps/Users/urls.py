from django.urls import path,include
from .views import UserRegisterView, LoginView, VerifyDocumentView,VerifyEmailView


urlpatterns =[
    path("register/", UserRegisterView.as_view(),name="user-register"),
    path('verify-email/<str:token>/', VerifyEmailView.as_view()),
    path('login/', LoginView.as_view()),
    path('verify-document/', VerifyDocumentView.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]