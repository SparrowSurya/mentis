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
            "password": "test@1234",
        }
        response = self.client.post(url, data)
        user_data = response.json()["user"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data.pop("password")
        for key, value in data.items():
            self.assertEqual(user_data[key], value)