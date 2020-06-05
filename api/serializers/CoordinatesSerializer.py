from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from api import utils, models


class CoordinatesSerializer(serializers.ModelSerializer):
    route_id = serializers.ReadOnlyField(source='route.id')

    class Meta:
        model = models.CoordinatesModel
        fields = ('lat', 'lon', 'route_id')

    def create(self, validated_data):
        route_id = validated_data.pop('route_id')
        route = self._retrieve_route(route_id)
        distance = utils.compute_route_distance_to_last_point(route, validated_data['lat'], validated_data['lon'])
        route.distance += distance
        route.save()
        coordinates = models.CoordinatesModel.objects.create(route=route, **validated_data)

        return coordinates

    def validate_lat(self, value):
        if not (-90 <= float(value) <= 90):
            raise serializers.ValidationError('Latitude out of range!')

        return value

    def validate_lon(self, value):
        if not (-180 <= float(value) <= 80):
            raise serializers.ValidationError('Longitude out of range!')

        return value

    @staticmethod
    def _retrieve_route(route_id: int) -> models.RouteModel:
        """
        Retrieves given route for adding coordinates. If the route ws not created today, exception is raised
        :param route_id:
        :return:
        :raises ParseError (ValidationError does not return a response in the correct format)
        """
        route = models.RouteModel.objects.get(pk=route_id)
        if route.local_date != timezone.localtime(timezone.now()).date():
            raise ParseError('Adding new way point to the route from the past days is not allowed.')

        return route
