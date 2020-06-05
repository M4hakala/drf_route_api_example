from django.test import TestCase
from django.utils import timezone
from api import models
from api import utils
from api.tests.utils.route_functions import create_route_with_coordinates
from parameterized import parameterized
import typing
from core.utils import local_today


class RouteHelperTestCase(TestCase):
    @parameterized.expand([
        ([], {"lat": -25.4025905, "lon": -49.3124416}, 0.),
        ([{"lat": -25.4025905, "lon": -49.3124416}], {"lat": -23.559798, "lon": -46.634971}, 339.),
        ([
            {"lat": -25.4025905, "lon": -49.3124416},
            {"lat": -23.559798, "lon": -46.634971},
        ], {"lat": 59.3258414, "lon": 17.70188}, 10889.),
    ])
    def test_compute_route_distance(self, route_coordinates: typing.List, coordinates: typing.Dict, expected):
        route = create_route_with_coordinates(route_coordinates)
        distance = utils.compute_route_distance_to_last_point(route, coordinates['lat'], coordinates['lon'])
        self.assertAlmostEqual(distance, expected, delta=5)

    def test_find_longest_route_from_longest_routes(self):
        dist = 10.
        date = timezone.now().date()
        route = models.RouteModel.objects.create()
        route.distance = dist
        route.save()
        models.LongestRouteModel.objects.create(route=route, route_date=date)
        longest_route = utils.find_longest_route(date)
        self.assertEqual(longest_route.distance, dist)

    @parameterized.expand([
        ([
            [
                {"lat": -25.4025905, "lon": -49.3124416},
                {"lat": -23.559798, "lon": -46.634971},
            ],
            [
                {"lat": -25.4025905, "lon": -49.3124416},
                {"lat": -23.559798, "lon": -46.634971},
                {"lat": 59.3258414, "lon": 17.70188},
            ],
        ], max),
        ([
            [
                {"lat": -25.4025905, "lon": -49.3124416},
            ],
        ], None),
    ])
    def test_find_longest_route_from_routes(self, routes, expected):
        date = local_today()
        distances = []
        for route in routes:
            route = create_route_with_coordinates(route)
            distances.append(route.distance)

        longest_route = utils.find_longest_route(date)
        if longest_route:
            self.assertEqual(longest_route.distance, expected(distances))
            longest_distance = models.LongestRouteModel.objects.get(route_date=date)
            self.assertEqual(longest_route, longest_distance.route)
        else:
            self.assertEqual(longest_route, expected)
