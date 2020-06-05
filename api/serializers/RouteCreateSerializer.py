from rest_framework import serializers
from api.models import RouteModel


class RouteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteModel
        fields = ('route_id', 'local_date')
