from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from core import models


class ReplyTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            username="testuser",
            password="testpassword",
        )
        self.client.force_authenticate(user=self.user)
        self.video = models.Video.objects.create(
            title="Test Video",
            description="This is a test video",
            thumbnail="test_thumbnail.jpg",
            file="test_video.mp4",
            created_by=self.user,
        )
        self.comment = models.Comment.objects.create(
            text="This is a test comment",
            created_by=self.user,
            video=self.video,
        )
        reply = models.CommentReply.objects.create(
            text="This is a test reply",
            created_by=self.user,
            comment=self.comment,
        )
        self.reply_list_url = reverse("reply:detail", args=[reply.id])
        self.reply = {
            "text": "This is a test reply",
        }

    def test_reply_detail(self):
        res = self.client.get(self.reply_list_url)
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data["text"], self.reply["text"])

    def test_reply_update(self):
        res = self.client.patch(self.reply_list_url, self.reply, format="json")
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(data)

    def test_reply_delete(self):
        res = self.client.delete(self.reply_list_url)
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(data)
