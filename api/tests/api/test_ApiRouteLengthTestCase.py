from django.urls import reverse, exceptions
from rest_framework import status
from .AbstractTestCase import AbstractTestCase
from parameterized import parameterized


class ApiRouteLengthTestCase(AbstractTestCase):
    def test_get_route_length(self):
        response = self.api_create_route()
        route_id = response.data['route_id']
        len_response = self.client.get(reverse(self.name_route_get_length, kwargs={'pk': route_id}))
        self.assertEqual(len_response.status_code, status.HTTP_200_OK)
        self.assertTrue(11750 < len_response.data['km'] < 11900)

    @parameterized.expand([
        (12, status.HTTP_404_NOT_FOUND),
        ('12', status.HTTP_404_NOT_FOUND),
        ('aa', exceptions.NoReverseMatch),
        (22.2, exceptions.NoReverseMatch),
    ])
    def test_get_route_length_incorrect_use(self, pk, expected):
        self._force_incorrect_usage(self.name_route_get_length, {'pk': pk}, expected)

    @parameterized.expand([
        ('put', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('patch', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('head', status.HTTP_404_NOT_FOUND),
        ('post', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('delete', status.HTTP_405_METHOD_NOT_ALLOWED),
    ])
    def test_get_route_length_with_not_allowed_methods(self, method, expected_code):
        url = reverse(AbstractTestCase.name_route_get_length, kwargs={'pk': 1})
        self._make_generic_request(url, method, expected_code)
