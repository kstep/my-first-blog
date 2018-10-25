from django import views
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, renderers
from rest_framework.response import Response

from blog.serializers import PostSerializer
from .forms import PostForm
from .models import Post


class PostViewSet(viewsets.ViewSet):
    renderer_classes = (renderers.TemplateHTMLRenderer,)

    def retrieve(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, template_name='blog/post_detail.html')

    def list(self, request):
        serializer = PostSerializer(Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date'), many=True)
        return Response(serializer.data, template_name='blog/post_list.html')

    def update(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            post = serializer.save(author=request.user,
                                   published_data=timezone.now())
            return self.retrieve(request, post.pk)
        else:
            return Response(serializer.data, template_name='blog/post_edit.html')

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(author=request.user,
                                   published_date=timezone.now())
            return self.retrieve(request, post.pk)
        else:
            return Response(serializer.data, template_name='blog/post_edit.html')


class PostNewView(views.View):
    template_name = 'blog/post_edit.html'
    def get(self, request):
        return render(request, self.template_name, {'form': PostForm()})


class PostEditView(views.View):
    template_name = 'blog/post_edit.html'
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(instance=post)
        return render(request, self.template_name, {'form': form})

