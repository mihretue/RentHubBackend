from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate
from apps.Users.serializers.registrationSerializer import UserRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserRegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Send verification link
        token = jwt.encode({'email': email}, settings.SECRET_KEY, algorithm='HS256')
        verify_url = f"http://localhost:3000/verify-email/{token}"

        send_mail(
            "Verify your email",
            f"Click the link to verify: {verify_url}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        return Response({'message': 'User registered, please verify email'}, status=201)
    
    
class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(email=payload['email'])
            user.email_verified = True
            user.save()
            return Response({'message': 'Email verified successfully'}, status=200)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired'}, status=400)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=400)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)

        if not user:
            return Response({'error': 'Invalid credentials'}, status=401)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
        
class VerifyDocumentView(APIView):
    def post(self, request):
        document_id = request.data.get('document_id')
        # your verification logic here...
        request.user.document_verified = True
        request.user.save()
        return Response({'message': 'Document verified successfully'})
