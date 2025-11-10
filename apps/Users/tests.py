import jwt
from django.conf import settings
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Full API paths
        self.register_url = '/api/users/register/'
        self.login_url = '/api/users/login/'
        self.verify_doc_url = '/api/users/verify-document/'
        self.verify_email_base = '/api/users/verify-email/'

        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "StrongPass123!"
        }

    def test_register_user_success(self):
        """✅ Register user successfully"""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())

    def test_register_duplicate_email(self):
        """❌ Duplicate email should fail"""
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_verify_email_success(self):
        """✅ Verify email using valid token"""
        user = User.objects.create_user(**self.user_data)
        token = jwt.encode({'email': user.email}, settings.SECRET_KEY, algorithm='HS256')
        url = f'{self.verify_email_base}{token}/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertTrue(user.email_verified)

    def test_verify_email_invalid_token(self):
        """❌ Invalid token should fail"""
        url = f'{self.verify_email_base}invalid_token/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_login_success(self):
        """✅ Login with correct credentials"""
        User.objects.create_user(**self.user_data)
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_failure(self):
        """❌ Login should fail with wrong credentials"""
        login_data = {"email": "wrong@example.com", "password": "wrongpass"}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_verify_document_success(self):
        """✅ Verify document endpoint for authenticated user"""
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)

        response = self.client.post(self.verify_doc_url, {"document_id": "123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

        user.refresh_from_db()
        self.assertTrue(user.document_verified)
