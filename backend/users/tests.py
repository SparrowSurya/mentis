from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class RootAPICallTest(APITestCase):

    def test_root_api_call(self):
        url = reverse("api:root")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserRegistrationTest(APITestCase):

    def test_user_registration(self):
        url = reverse("api:user-register")
        data = {
            "first_name": "first-name",
            "last_name": "last-name",
            "email": "test@example.com",
            "phone_no": "9876543210",
            "password1": "test@1234",
            "password2": "test@1234",
        }
        response = self.client.post(url, data)
        user_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data.pop("password1")
        data.pop("password2")
        for key, value in data.items():
            self.assertEqual(user_data[key], value)


class UserAuthenticationTest(APITestCase):

    wrong_password = "wrong[assword]"
    password = "password1234"

    login_url = reverse("api:user-login")
    logout_url = reverse("api:user-logout")

    def setUp(self):
        assert self.password != self.wrong_password

        self.user = User(**{
            "first_name": "first-name",
            "last_name": "last-name",
            "email": "test@example.com",
            "phone_no": "9876543210",
        })
        self.user.set_password(self.password)
        self.user.save()

    def test_login_success(self):
        credentials = {"email": "test@example.com", "password": self.password}
        response = self.client.post(self.login_url, credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_failure_wrong_password(self):
        credentials = {"email": "test@example.com", "password": self.wrong_password}
        response = self.client.post(self.login_url, credentials)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_success(self):
        refresh = RefreshToken.for_user(self.user)
        access = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        response = self.client.post(self.logout_url, {"refresh": str(refresh)})
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_invalid_token(self):
        response = self.client.post(self.logout_url, {"refresh": "invalidtoken"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_bad_request(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
