from django.conf import settings
from django.db.models import Count
from api import models
from api import serializers
from typing import Optional
from geopy.distance import geodesic
from datetime import date


def compute_route_distance_to_last_point(route: models.RouteModel, lat: float, lon: float, unit: str = 'km') -> float:
    """
    Calculates distance between given point and last point of the route
    :param route: route model
    :param lat: latitude
    :param lon: longitude
    :param unit: distance unit (default = kilometers)
    :return:
    """
    if route.coordinates.count() == 0:
        distance = 0.
    else:
        last_distance = route.coordinates.last()
        distance = getattr(
            geodesic(
                (float(last_distance.lat), float(last_distance.lon)),
                (float(lat), float(lon)),
                **{'ellipsoid': settings.GEO_ELLIPSOID}
            ),
            unit
        )

    return distance


def find_longest_route(route_date: date) -> Optional[models.RouteModel]:
    """
    Returns longest route at given date. If longest route is not present in its data table it will be calculated from
    routes included in routes table if present.
    :param route_date: lookup date of longest route
    :return:
    """
    longest_route_query = models.LongestRouteModel.objects.filter(route_date=route_date)
    if longest_route_query.exists():
        route = longest_route_query.first().route
    else:
        route_query = models.RouteModel.objects\
            .annotate(number_of_coordinates=Count('coordinates'))\
            .filter(number_of_coordinates__gt=0)\
            .filter(local_date=route_date)\
            .filter(distance__gt=0)\
            .order_by('-distance')

        if not route_query.exists():
            return None

        route = route_query.first()
        longest_route_serializer = serializers.LongestRouteWithRouteContextSerializer(
            route=route, data={'route_date': route_date}
        )
        if longest_route_serializer.is_valid():
            longest_route_serializer.save()

    return route
