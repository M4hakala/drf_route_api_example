from rest_framework import serializers
from api.models import RouteModel


class RouteDistanceSerializer(serializers.ModelSerializer):
    km = serializers.FloatField(source='distance', read_only=True)

    class Meta:
        model = RouteModel
        fields = ('route_id', 'km')
