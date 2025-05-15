from django.urls import path
from .views import BannerView

urlpatterns = [
    path('starter_banner/', BannerView.as_view(), name='banner-view'),
]
