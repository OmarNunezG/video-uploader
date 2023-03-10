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

    def test_like_comment_forbidden(self):
        """Test liking a comment"""
        url = reverse("comment:like", args=[self.comment.id])
        res = self.client.post(url)
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(data["status"], "403")
        self.assertEqual(data["title"], "Forbidden")

    def test_dislike_comment_forbidden(self):
        """Test unliking a comment"""
        url = reverse("comment:like", args=[self.comment.id])
        res = self.client.delete(url)
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(data["status"], "403")
        self.assertEqual(data["title"], "Forbidden")

    def test_like_comment_success(self):
        """Test liking a comment"""
        user = get_user_model().objects.create(
            first_name="Test",
            last_name="User",
            username="testuser2",
            email="testusername2@example.com",
            password="testpass",
        )

        url = reverse("comment:like", args=[self.comment.id])
        self.client.force_authenticate(user=user)
        res = self.client.post(url)
        data = res.data
        self.comment.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(data)
        self.assertEqual(self.comment.likes, 1)

    def test_dislike_comment_success(self):
        """Test unliking a comment"""
        user = get_user_model().objects.create(
            first_name="Test",
            last_name="User",
            username="testuser2",
            email="testusername2@example.com",
            password="testpass",
        )
        models.CommentLike.objects.create(liked_by=user, comment=self.comment)
        self.comment.likes = 1
        self.comment.save()

        url = reverse("comment:like", args=[self.comment.id])
        self.client.force_authenticate(user=user)
        res = self.client.delete(url)
        data = res.data
        self.comment.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(data)
        self.assertEqual(self.comment.likes, 0)

    def test_retieve_comment_replies_success(self):
        """Test retrieve comment replies"""
        user = get_user_model().objects.create(
            first_name="Test",
            last_name="User",
            username="testuser2",
            email="testusername2@example.com",
            password="testpass",
        )
        models.CommentReply.objects.create(
            text="Test reply", created_by=user, comment=self.comment
        )

        url = reverse("comment:reply", args=[self.comment.id])
        res = self.client.get(url)
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)

    def test_create_comment_reply_success(self):
        """Test creating a comment reply"""
        user = get_user_model().objects.create(
            first_name="Test",
            last_name="User",
            username="testuser2",
            email="testusername2@example.com",
            password="testpass",
        )

        payload = {"text": "Test reply"}
        url = reverse("comment:reply", args=[self.comment.id])
        self.client.force_authenticate(user=user)
        res = self.client.post(url, payload, format="json")
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(data)
