from rest_framework import permissions, generics


class RouteApiView(generics.CreateAPIView, generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
