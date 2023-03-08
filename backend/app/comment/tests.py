from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from core import models


class CommentPublicAPITests(APITestCase):
    """Test the publicly available comment API"""

    def setUp(self):
        self.user = get_user_model().objects.create(
            first_name="Test",
            last_name="User",
            username="testuser",
            email="testuser@example.com",
            password="testpass",
        )
        self.video = models.Video.objects.create(
            title="Test Video",
            description="Test Video Description",
            thumbnail="wii.jpg",
            file="wii.mp4",
            created_by=self.user,
        )
        self.comment = models.Comment.objects.create(
            text="Test comment", created_by=self.user, video=self.video
        )

    def test_retrieve_comment(self):
        """Test retrieving a comment"""
        url = reverse("comment:detail", args=[self.comment.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["text"], self.comment.text)


class CommentPrivateAPITests(APITestCase):
    """Test the private comment API"""

    def setUp(self):
        self.user = get_user_model().objects.create(
            first_name="Test",
            last_name="User",
            username="testuser",
            email="testuser@example.com",
            password="testpass",
        )
        self.video = models.Video.objects.create(
            title="Test Video",
            description="Test Video Description",
            thumbnail="wii.jpg",
            file="wii.mp4",
            created_by=self.user,
        )
        self.comment = models.Comment.objects.create(
            text="Test comment", created_by=self.user, video=self.video
        )
        self.client.force_authenticate(user=self.user)

    def test_update_comment(self):
        """Test updating a comment"""
        url = reverse("comment:detail", args=[self.comment.id])
        payload = {"text": "Updated comment"}
        self.client.force_authenticate(user=self.user)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["text"], payload["text"])

    def test_update_comment_unauthorized(self):
        """Test updating a comment as unauthorized user"""
        url = reverse("comment:detail", args=[self.comment.id])
        payload = {"text": "Updated comment"}
        self.client.force_authenticate(user=None)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_comment(self):
        """Test deleting a comment"""
        url = reverse("comment:detail", args=[self.comment.id])
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_comment_unauthorized(self):
        """Test deleting a comment as unauthorized user"""
        url = reverse("comment:detail", args=[self.comment.id])
        self.client.force_authenticate(user=None)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)