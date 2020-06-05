from rest_framework import permissions, generics
from api import serializers, models


class DetailRouteApiView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RouteSerializer
    queryset = models.RouteModel.objects.all()
