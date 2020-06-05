from rest_framework import serializers
from api.models import RouteModel
from api.serializers import CoordinatesSerializer


class RouteSerializer(serializers.ModelSerializer):
    coordinates = CoordinatesSerializer(many=True, read_only=True)
    km = serializers.FloatField(source='distance', read_only=True)

    class Meta:
        model = RouteModel
        fields = ('route_id', 'local_date', 'coordinates', 'km')
