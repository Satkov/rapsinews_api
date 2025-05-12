import json

from django.core.cache import cache
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination

from .cache import key_for, TTL
from .models import Post
from .serializers import PostSerializer


class StandardResultsSetPagination(LimitOffsetPagination):
    """Default Limit‑Offset paginator used across all API views."""

    default_limit = 10
    max_limit = 50
    limit_query_param = "limit"
    offset_query_param = "offset"

class PostListAPIView(ListAPIView):
    queryset = Post.objects.all().order_by("-published")
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        cache_key = key_for(request)
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(json.loads(cached))

        # обычный CBV‑поток
        response = super().list(request, *args, **kwargs)

        # сохраняем «готовый» JSON
        rendered = JSONRenderer().render(response.data).decode()
        cache.set(cache_key, rendered, TTL)
        return response


class BookmarkPostsAPIView(APIView):
    """Return posts whose IDs are supplied in the request body."""

    pagination_class = StandardResultsSetPagination

    def post(self, request):
        post_ids = request.data.get("ids", [])

        if not isinstance(post_ids, list) or not all(
            isinstance(post_id, int) for post_id in post_ids
        ):
            error_msg = {"error": "Invalid input. Expected a list of integers."}
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

        posts = Post.objects.filter(id__in=post_ids)
        if not posts.exists():
            not_found_msg = {"message": "No posts found with the given IDs."}
            return Response(not_found_msg, status=status.HTTP_404_NOT_FOUND)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class SearchPostsAPIView(APIView):
    """Search posts by title using the 'query' URL parameter."""

    pagination_class = StandardResultsSetPagination

    def get(self, request):
        query = request.query_params.get("query")
        if not query:
            error_msg = {"error": "Query parameter 'query' is required."}
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

        posts = Post.objects.filter(title__icontains=query)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
