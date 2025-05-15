from rest_framework import serializers
from .models import Banner, Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['url']

class BannerSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = Banner
        fields = ['title', 'images', 'link', 'is_active']
