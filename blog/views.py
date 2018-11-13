from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from rest_framework import viewsets, renderers
from rest_framework.response import Response

from blog.serializers import PostSerializer
from .models import Post


class PostViewSet(viewsets.ViewSet):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)

    def retrieve(self, request, pk, format='html'):
        try:
            post = PostSerializer(Post.objects.get(pk=pk))
        except Post.DoesNotExist:
            post = PostSerializer()

        edit = format == 'html' and request.query_params.get('edit', False)
        return Response({'post': post if edit else post.data},
                        template_name='blog/post_edit.html' if edit else 'blog/post_detail.html')

    def list(self, request, format='html'):
        edit = format == 'html' and request.query_params.get('edit', False)

        if edit:
            return Response({'post': PostSerializer()}, template_name='blog/post_edit.html')
        else:
            serializer = PostSerializer(Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date'), many=True)
            return Response({'posts': serializer.data}, template_name='blog/post_list.html')

    def update(self, request, pk, format='html'):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            post = serializer.save(author=request.user,
                                   published_date=timezone.now())
            return self.retrieve(request, post.pk, format)
        else:
            return Response({'errors': serializer.errors}, template_name='blog/post_edit.html', status=400)

    def create(self, request, format='html'):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(author=request.user,
                                   published_date=timezone.now())
            return self.retrieve(request, post.pk, format)
        else:
            return Response({'errors': serializer.errors}, template_name='blog/post_edit.html', status=400)
