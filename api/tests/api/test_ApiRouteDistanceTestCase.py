from django.urls import reverse, exceptions
from django.utils import timezone
from django.core.cache import cache
from rest_framework import status
from api import models
from .AbstractTestCase import AbstractTestCase
from parameterized import parameterized
import datetime


class ApiRouteDistanceTestCase(AbstractTestCase):
    @parameterized.expand([
        (timezone.now() - datetime.timedelta(days=1), None, status.HTTP_200_OK),
        (timezone.now(), timezone.now() - datetime.timedelta(days=1), status.HTTP_404_NOT_FOUND),
        (timezone.now(), None, status.HTTP_400_BAD_REQUEST),
    ])
    def test_get_distance(self, create_date, request_date, expected):
        if not request_date:
            request_date = create_date
        response = self.api_create_route()
        route_id = response.data['route_id']
        route = models.RouteModel.objects.get(pk=route_id)
        route.local_date = create_date.date()
        route.save()

        url = reverse(
            self.name_route_longest_distance,
            kwargs={'year': request_date.year, 'month': f"{request_date.month:02d}", 'day': f"{request_date.day:02d}"}
        )
        cache.clear()
        distance_response = self.client.get(url)
        self.assertEqual(distance_response.status_code, expected)

    @parameterized.expand([
        ('put', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('patch', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('post', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('delete', status.HTTP_405_METHOD_NOT_ALLOWED),
    ])
    def test_get_distance_with_not_allowed_methods(self, method, expected_code):
        date = timezone.now().date() - datetime.timedelta(days=1)
        url = reverse(
            self.name_route_longest_distance,
            kwargs={'year': date.year, 'month': f"{date.month:02d}", 'day': f"{date.day:02d}"}
        )
        self._make_generic_request(url, method, expected_code)

    @parameterized.expand([
        ((2020, 1, 1), exceptions.NoReverseMatch),
        (('2020', '01', '41'), status.HTTP_400_BAD_REQUEST),
        (('aaaa', '01', '41'), exceptions.NoReverseMatch),
    ])
    def test_get_distance_incorrect_usage(self, date_params, expected):
        self._force_incorrect_usage(
            self.name_route_longest_distance,
            dict(year=date_params[0], month=date_params[1], day=date_params[2]),
            expected
        )
