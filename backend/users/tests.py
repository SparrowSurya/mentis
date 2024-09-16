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

    register_url = reverse("api:user-register")

    def test_user_registration_success(self):
        data = {
            "email": "test@example.com",
            "phone_no": "9876543210",
            "password1": "test@1234",
            "password2": "test@1234",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data.pop("password1")
        data.pop("password2")
        user_data = response.json()
        for key, value in data.items():
            self.assertEqual(user_data[key], value)

    def test_registration_fails_on_mismatch_passords(self):
        data = {
            "email": "test@example.com",
            "password1": "test@1234",
            "password2": "wrong-password",
        }
        assert data["password1"] != data["password2"]
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserAuthenticationTest(APITestCase):

    wrong_password = "wrongPassword"
    password = "password1234"

    login_url = reverse("api:user-login")
    logout_url = reverse("api:user-logout")

    def setUp(self):
        assert self.password != self.wrong_password
        self.user = User.objects.create_user(
            email="test@example.com",
            password=self.password,
        )

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


class UserUpdationTest(APITestCase):

    email = "user@example.com"
    password = "password"
    wrong_password = "wrongpassword"

    login_url = reverse("api:user-login")
    logout_url = reverse("api:user-logout")
    user_update_url = reverse("api:user-update")
    user_password_update_url = reverse("api:user-update-password")

    def setUp(self):
        assert self.password != self.wrong_password

        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
        )
        credentials = {
            "email": self.email,
            "password": self.password,
        }
        response = self.client.post(self.login_url, credentials)
        tokens = response.json()

        self.access_tok = tokens["access"]
        self.refresh_tok = tokens["refresh"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_tok}")

    def test_user_updation_success(self):
        data = {
            "first_name": "user",
            "last_name": "_007",
            "email": "newuser@example.com",
            "phone_no": "9876543211",
        }
        response = self.client.put(self.user_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_data = response.json()["user"]
        for key, value in data.items():
            self.assertEqual(value, updated_data[key])

    def test_user_updation_failure_on_missing_required_field(self):
        data = {
            "first_name": "user",
            "last_name": "_007",
            "email": "",
            "phone_no": "9876543211",
        }
        response = self.client.put(self.user_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_password_updation_then_login_success(self):
        password1 = password2 ="new-password"
        assert password1 == password2
        data = {
            "old_password": self.password,
            "password1": password1,
            "password2": password2,
        }
        response = self.client.put(self.user_password_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.post(self.logout_url, {"refresh": self.refresh_tok})

        credentials = {
            "email": self.email,
            "password": password1,
        }
        response = self.client.post(self.login_url, credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_password_updation_failure_on_mismatch(self):
        password1 = "new-password"
        password2 = "no-new-password"
        assert password1 != password2
        data = {
            "old_password": self.password,
            "password1": password1,
            "password2": password2,
        }
        response = self.client.put(self.user_password_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_password_updation_failure_on_wrong_old_password(self):
        old_password = "wrong-old-password"
        password1 = password2 ="new-password"

        assert old_password != self.password
        assert password1 == password2

        data = {
            "old_password": old_password,
            "password1": password1,
            "password2": password2,
        }
        response = self.client.put(self.user_password_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
