from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Banner
from .serializers import BannerSerializer

class BannerView(APIView):
    """
    Эндпоинт для получения текущего активного баннера.
    """
    def get(self, request):
        banner = Banner.objects.filter(is_active=True).first()
        if not banner:
            return Response({"detail": "Активный баннер не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BannerSerializer(banner)
        return Response(serializer.data, status=status.HTTP_200_OK)
