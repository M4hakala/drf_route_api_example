from django.urls import reverse
from rest_framework import status
from api import models
from .AbstractTestCase import AbstractTestCase
from parameterized import parameterized


class ApiRouteCreateTestCase(AbstractTestCase):
    def test_create_route(self) -> None:
        _ = self.api_init_route()

        self.assertIsNotNone(models.RouteModel.objects.first())
        self.assertEqual(models.RouteModel.objects.count(), 1)

    @parameterized.expand([
        ('put', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('patch', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('head', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('get', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('delete', status.HTTP_405_METHOD_NOT_ALLOWED),
    ])
    def test_create_route_with_not_allowed_methods(self, method, expected_code):
        url = reverse(AbstractTestCase.name_route_create)
        self._make_generic_request(url, method, expected_code)
