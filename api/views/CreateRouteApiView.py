from rest_framework import permissions, generics
from api import serializers


class CreateRouteApiView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RouteCreateSerializer
