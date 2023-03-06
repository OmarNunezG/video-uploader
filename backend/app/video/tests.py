from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from core import models


class PublicVideoApiTests(APITestCase):
    """Test the publicly available video API"""

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

    def test_retrieve_videos_success(self):
        """Test retrieving a list of videos"""
        url = reverse("video:list")
        res = self.client.get(url)

        data = res.data

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["next"], None)
        self.assertEqual(data["previous"], None)
        self.assertEqual(len(data["results"]), 1)

    def test_retreive_video_success(self):
        """Test retrieving a single video"""
        url = reverse("video:detail", args=[self.video.id])
        res = self.client.get(url)

        data = res.data

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data["id"], self.video.id)
        self.assertEqual(data["title"], self.video.title)
        self.assertEqual(data["description"], self.video.description)
        self.assertEqual(
            data["thumbnail"],
            f"/media/{self.user.id}/thumbnails/{self.video.thumbnail}",
        )
        self.assertEqual(
            data["file"], f"/media/{self.user.id}/videos/{self.video.file}"
        )
        self.assertEqual(
            data["created_at"],
            self.video.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        )
        self.assertEqual(data["created_by"], self.video.created_by.username)


class PrivateVideoApiTests(APITestCase):
    """Test the private video API"""

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
        self.client.force_authenticate(user=self.user)

    def test_update_video_success(self):
        """Test updating a video"""
        url = reverse("video:detail", args=[self.video.id])

        payload = {
            "title": "Updated Video",
            "description": "Updated Video Description",
        }

        res = self.client.patch(url, payload, format="json")

        self.video.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(payload["title"], self.video.title)
        self.assertEqual(payload["description"], self.video.description)

    def test_delete_video_success(self):
        """Test deleting a video"""
        url = reverse("video:detail", args=[self.video.id])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_comment_video_success(self):
        """Test commenting on a video"""
        url = reverse("video:comment", args=[self.video.id])

        payload = {"text": "Test Comment"}

        res = self.client.post(url, payload, format="json")
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("Location", res.headers)
        self.assertEqual(data["text"], payload["text"])
        self.assertEqual(data["video"], self.video.id)

    def test_retrieve_comments_success(self):
        """Test retrieving comments on a video"""
        models.Comment.objects.create(
            text="Test Comment 1", video=self.video, created_by=self.user
        )
        models.Comment.objects.create(
            text="Test Comment 2", video=self.video, created_by=self.user
        )

        url = reverse("video:comment", args=[self.video.id])
        res = self.client.get(url)

        data = res.data

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 2)
