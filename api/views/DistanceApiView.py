from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
from rest_framework import exceptions, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from api import serializers, utils
from core.utils import local_today
import datetime


class DistanceApiView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.RouteSerializer

    @method_decorator(cache_page(settings.DISTANCE_VIEW_CACHE_TIMEOUT))
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves longest route at given date. Preview of current day routes is not allowed.
        """
        route_date = self._get_date_from_request()
        if route_date == local_today():
            raise exceptions.ValidationError('Today\'s routes are not yet completed.')

        route = utils.find_longest_route(route_date)
        if not route:
            raise exceptions.NotFound(f'No routes found for date {route_date}.')

        serializer = serializers.RouteSerializer(route)

        return Response(serializer.data)

    def _get_date_from_request(self) -> datetime.date:
        """
        Converts date attributes from url to date
        :raises exceptions.ValidationError exception when date attributes are out of range
        :return:
        """
        try:
            return datetime.date(
                year=int(self.kwargs.get('year')),
                month=int(self.kwargs.get('month')),
                day=int(self.kwargs.get('day'))
            )
        except ValueError:
            raise exceptions.ValidationError('Date is out of range.')
