from api import serializers, models
import typing


def create_route_with_coordinates(coordinates_list: typing.List[typing.Dict]) -> models.RouteModel:
    route = models.RouteModel.objects.create()
    for coordinates in coordinates_list:
        serializer = serializers.CoordinatesSerializer(data=coordinates)
        if serializer.is_valid():
            serializer.save(route_id=route.route_id)
            route.refresh_from_db()
        route.coordinates.add(serializer.instance)

    return route
