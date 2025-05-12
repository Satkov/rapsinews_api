from django.urls import path
from .views import PostListAPIView, BookmarkPostsAPIView, SearchPostsAPIView

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='post-list'),
    path('bookmarks/', BookmarkPostsAPIView.as_view(), name='bookmark-posts'),
    path('search/', SearchPostsAPIView.as_view(), name='search-posts'),
]