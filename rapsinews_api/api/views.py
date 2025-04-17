from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

class PostListAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all().order_by('-published')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)