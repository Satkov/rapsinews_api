from rest_framework.generics import ListAPIView
from .models import Post
from .serializers import PostSerializer

class PostListAPIView(ListAPIView):
    queryset = Post.objects.all().order_by('-published')
    serializer_class = PostSerializer