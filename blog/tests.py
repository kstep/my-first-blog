from django.utils import timezone

from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.test import APIClient

from blog.models import Post
from blog.serializers import PostSerializer


class BlogAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user')
        self.posts = [
            Post.objects.create(title="post1",
                                text="text1",
                                author=self.user,
                                published_date=timezone.now()),
            Post.objects.create(title="post2",
                                text="text2",
                                author=self.user,
                                published_date=timezone.now())
        ]
        self.client = APIClient()

    def tearDown(self):
        pass

    def test_posts_list(self):
        expected = {
            'posts': [
                PostSerializer(p).data for p in self.posts
            ]
        }

        response = self.client.get('/posts/')

        self.assertEqual(response.data, expected)

    def test_posts_retrieve(self):
        post = self.posts[0]

        expected = {'post': PostSerializer(post).data}
        response = self.client.get('/posts/{}/'.format(post.id))

        self.assertEqual(response.data, expected)

    def test_posts_create(self):
        post = {
            'title': 'Title3',
            'text': 'Text3'
        }

        self.client.force_authenticate(self.user)
        response = self.client.post('/posts/', data=post)

        data = response.data
        self.assertIn('post', data)
        self.assertEqual(data['post']['title'], post['title'])
        self.assertEqual(data['post']['text'], post['text'])
        
