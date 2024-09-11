from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


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