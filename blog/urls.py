from rest_framework.routers import DefaultRouter

from blog.views import PostViewSet


class PostAsPutRouter(DefaultRouter):
    def get_method_map(self, viewset, method_map):
        method_map = super(PostAsPutRouter, self).get_method_map(viewset, method_map)
        if 'put' in method_map and 'post' not in method_map:
            method_map['post'] = method_map['put']
        return method_map


router = PostAsPutRouter()
router.register('posts', PostViewSet, basename='post')

urlpatterns = router.urls
