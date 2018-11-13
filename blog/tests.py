import json

from django.utils import timezone

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIClient, APIRequestFactory

from blog.models import Post
from blog.serializers import PostSerializer
from blog.views import PostViewSet


class BlogAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        self.posts = [
            Post.objects.create(title="post1", text="text1", author=self.user, published_date=timezone.now()),
            Post.objects.create(title="post2", text="text2", author=self.user, published_date=timezone.now())
        ]
        self.client = APIClient()

    def tearDown(self):
        pass

    def test_list_posts(self):
        factory = APIRequestFactory()
        request = factory.get('/posts/', format='json')
        view = PostViewSet.as_view({'get': 'list'})
        response = view(request)

        response = APIClient().get('/posts/')
        expected = {'posts': [
                PostSerializer(p).data for p in self.posts
            ]
        }
        self.assertEqual(response.data, expected)
