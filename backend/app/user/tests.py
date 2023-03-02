from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core import models

format = "json"


class PublicUserApiTests(APITestCase):
    """Test the users API (public)"""

    def test_register_valid_user_success(self):
        """Test registering user with valid payload is successful"""
        url = reverse("user:list")

        payload = {
            "attributes": {
                "first_name": "test",
                "last_name": "name",
                "email": "test.name@example.com",
                "username": "testuser",
                "password": "testpass",
            },
        }

        res = self.client.post(url, payload, format=format)
        data = res.data
        req_attributes = payload["attributes"]
        res_attributes = data["attributes"]

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("Location", res.headers)

        self.assertIn("id", data)

        self.assertEqual(
            res_attributes["first_name"], req_attributes["first_name"]
        )
        self.assertIsNone(res_attributes["middle_name"])
        self.assertEqual(
            res_attributes["last_name"], req_attributes["last_name"]
        )
        self.assertEqual(res_attributes["email"], req_attributes["email"])
        self.assertEqual(
            res_attributes["username"], req_attributes["username"]
        )

        self.assertNotIn("id", res_attributes)
        self.assertNotIn("password", res_attributes)

    def test_register_invalid_user_fails(self):
        """Test registering user with invalid payload fails"""
        url = reverse("user:list")

        payload = {
            "attributes": {
                "first_name": "",
                "last_name": "",
                "email": "",
                "username": "",
                "password": "",
            },
        }

        res = self.client.post(url, payload, format=format)
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(data["status"], str(status.HTTP_400_BAD_REQUEST))
        self.assertEqual(data["title"], "Bad Request")
        self.assertIn("detail", data)

    def test_login_valid_user_success(self):
        """Test logging in user with valid credentials is successful"""
        get_user_model().objects.create(
            first_name="test",
            last_name="name",
            email="test@example.com",
            username="testuser",
            password="testpass123",
        )

        url = reverse("user:pair-token")

        payload = {
            "username": "testuser",
            "password": "testpass123",
        }

        res = self.client.post(url, payload, format=format)
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", data)
        self.assertIn("refresh", data)

    def test_login_invalid_user_fails(self):
        """Test logging in user with invalid credentials fails"""
        url = reverse("user:pair-token")

        payload = {
            "username": "testuser",
            "password": "wrongpass",
        }

        res = self.client.post(url, payload, format=format)
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", data)

    def test_retrieve_users_success(self):
        """Test retrieving users is successful"""
        self.user = get_user_model().objects.create(
            first_name="test",
            last_name="name",
            email="test@example.com",
            username="testuser",
            password="testpass123",
        )

        url = reverse("user:list")

        res = self.client.get(url, format=format)
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)


class PrivateUserApiTests(APITestCase):
    """Test the users API (private)"""

    def setUp(self):
        self.user = get_user_model().objects.create(
            first_name="test",
            last_name="name",
            email="test@example.com",
            username="testuser",
            password="testpass123",
        )
        self.user.is_staff = True
        self.user.is_admin = True

        self.client.force_authenticate(user=self.user)

        models.Video.objects.create(
            title="test video",
            description="test description",
            thumbnail="test.png",
            file="test.mp4",
            created_by=self.user,
        )

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user is successful"""
        url = reverse("user:profile")

        res = self.client.get(url, format=format)
        data = res.data
        attributes = data["attributes"]

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(data["id"], self.user.id)

        self.assertEqual(attributes["first_name"], self.user.first_name)
        self.assertIsNone(attributes["middle_name"])
        self.assertEqual(attributes["last_name"], self.user.last_name)
        self.assertEqual(attributes["username"], self.user.username)
        self.assertEqual(attributes["email"], self.user.email)

    def test_retrieve_profile_unauthorized_fails(self):
        """Test retrieving profile for unauthorized user fails"""
        self.client.force_authenticate(user=None)

        url = reverse("user:profile")

        res = self.client.get(url, format=format)
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", data)

    def test_update_profile_success(self):
        """Test updating the user profile for authenticated user"""
        url = reverse("user:profile")

        payload = {
            "attributes": {
                "first_name": "new",
            },
        }

        res = self.client.patch(url, payload, format=format)
        data = res.data
        attributes = data["attributes"]

        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(attributes["first_name"], self.user.first_name)

    def test_update_profile_invalid_fails(self):
        """Test updating the user profile with invalid payload fails"""
        url = reverse("user:profile")

        payload = {
            "attributes": {
                "first_name": "",
            },
        }

        res = self.client.patch(url, payload, format=format)
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(data["status"], str(status.HTTP_400_BAD_REQUEST))
        self.assertEqual(data["title"], "Bad Request")
        self.assertIn("detail", data)

    def test_retrieve_user_success(self):
        """Test retrieving user is successful"""
        url = reverse("user:detail", args=[self.user.id])

        res = self.client.get(url, format=format)
        data = res.data
        attributes = data["attributes"]

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(data["id"], self.user.id)

        self.assertEqual(attributes["first_name"], self.user.first_name)
        self.assertIsNone(attributes["middle_name"])
        self.assertEqual(attributes["last_name"], self.user.last_name)
        self.assertEqual(attributes["username"], self.user.username)
        self.assertEqual(attributes["email"], self.user.email)

    def test_delete_user_success(self):
        """Test deleting user is successful"""
        url = reverse("user:detail", args=[self.user.id])

        res = self.client.delete(url, format=format)
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(data, None)

    def test_delete_user_unauthorized_fails(self):
        """Test deleting user for unauthorized user fails"""
        self.client.force_authenticate(user=None)

        url = reverse("user:detail", args=[self.user.id])

        res = self.client.delete(url, format=format)
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", data)

    def test_delete_user_invalid_fails(self):
        """Test deleting user with invalid id fails"""
        url = reverse("user:detail", args=[999])

        res = self.client.delete(url, format=format)
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", data)

    def test_retrieve_videos_success(self):
        """Test retrieving videos is successful"""
        url = reverse("user:videos", args=[self.user.id])

        res = self.client.get(url, format=format)
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
