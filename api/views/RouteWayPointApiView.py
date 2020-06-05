from rest_framework import permissions, generics, exceptions
from api import serializers, models


class RouteWayPointApiView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.CoordinatesSerializer

    def perform_create(self, serializer):
        try:
            serializer.save(route_id=self.kwargs['pk'])
        except models.RouteModel.DoesNotExist:
            raise exceptions.NotFound('Given route does not exists.')
