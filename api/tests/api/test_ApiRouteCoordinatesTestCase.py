from django.urls import reverse
from rest_framework import status
from .AbstractTestCase import AbstractTestCase
from parameterized import parameterized
import json


class ApiRouteCoordinatesTestCase(AbstractTestCase):
    def test_add_way_points(self):
        self.api_create_route()

    @parameterized.expand([
        ('put', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('patch', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('head', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('get', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('delete', status.HTTP_405_METHOD_NOT_ALLOWED),
    ])
    def test_route_add_way_point_with_not_allowed_methods(self, method, expected_code):
        url = reverse(self.name_route_add_way_point, kwargs={'pk': 1})
        self._make_generic_request(url, method, expected_code)

    def test_route_add_way_point_without_headers(self):
        response = self.api_init_route()
        response = self.client.generic(
            'post',
            reverse(self.name_route_add_way_point, kwargs={'pk': response.data['route_id']}),
            {"lat": -25.4025905, "lon": -49.3124416},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        return response

    @parameterized.expand([
        (1, 'aa', '-49.3124416', status.HTTP_400_BAD_REQUEST, ('lat', 0, 'A valid number is required.')),
        (1, '-23.559798', '--', status.HTTP_400_BAD_REQUEST, ('lon', 0, 'A valid number is required.')),
        (1, '-23.559798', '-181.0000', status.HTTP_400_BAD_REQUEST, ('lon', 0, 'Longitude out of range!')),
        (1, '-23.559798', '81.0000', status.HTTP_400_BAD_REQUEST, ('lon', 0, 'Longitude out of range!')),
        (1, '-91.0000', '-49.3124416', status.HTTP_400_BAD_REQUEST, ('lat', 0, 'Latitude out of range!')),
        (1, '91.0000', '-49.3124416', status.HTTP_400_BAD_REQUEST, ('lat', 0, 'Latitude out of range!')),
        (12, '-23.559798', '-49.3124416', status.HTTP_404_NOT_FOUND, ('detail', 0, 'Given route does not exists')),
    ])
    def test_route_add_way_point_incorrect_use(self, pk, lat, lon, expected_code, expected_msg):
        self.api_init_route()
        url = reverse(self.name_route_add_way_point, kwargs={'pk': pk})
        response = self._make_generic_request(url, 'post', expected_code, json.dumps({"lat": lat, "lon": lon}))
        response_data = response.data[expected_msg[0]]
        response_msg = str(response_data[expected_msg[1]]) if isinstance(response_data, list) else str(response_data)
        self.assertIn(expected_msg[2], response_msg)
