from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.Users.serializers.registrationSerializer import UserRegisterSerializer

User = get_user_model()

class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            # Check if user exists
            if User.objects.filter(email=email).exists():
                return Response(
                    {"message": "User with this email already exists"},
                    status=status.HTTP_409_CONFLICT
                )
            user = serializer.save()
            # Return user data without password
            user_data = UserRegisterSerializer(user).data
            return Response(
                {"user": user_data, "message": "User created successfully"},
                status=status.HTTP_201_CREATED
            )

        # Validation errors
        return Response(
            {"message": "Invalid request data", "errors": serializer.errors},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
