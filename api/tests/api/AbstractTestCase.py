from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from api import urls
import inspect


class AbstractTestCase(APITestCase):
    name_route_create = f"api:{urls.URL_NAMES['route.route_create']}"
    name_route_get_length = f"api:{urls.URL_NAMES['route.route_get_length']}"
    name_route_add_way_point = f"api:{urls.URL_NAMES['route.route_add_way_point']}"
    name_route_longest_distance = f"api:{urls.URL_NAMES['route.get_longest_route']}"

    def api_init_route(self):
        response = self.client.post(reverse(self.name_route_create), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        return response

    def api_create_route(self):
        response = self.api_init_route()
        route_id = response.data['route_id']
        coordinates = [
            {"lat": -25.4025905, "lon": -49.3124416},
            {"lat": -23.559798, "lon": -46.634971},
            {"lat": 59.3258414, "lon": 17.70188},
            {"lat": 54.273901, "lon": 18.591889}
        ]
        url = reverse(self.name_route_add_way_point, kwargs={'pk': route_id})
        for point in coordinates:
            coordinate_response = self.client.post(url, point, format='json')
            self.assertEqual(coordinate_response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(float(coordinate_response.data.get('lat')), float(point['lat']))
            self.assertEqual(float(coordinate_response.data.get('lon')), float(point['lon']))

        return response

    def _make_generic_request(self, url, method, expected, data=None, content_type='application/json'):
        response = self.client.generic(method, url, data, content_type)
        self.assertEqual(response.status_code, expected)

        return response

    def _force_incorrect_usage(self, route_name, reverse_params, expected):
        if inspect.isclass(expected) and issubclass(expected, Exception):
            self.assertRaises(expected, reverse, route_name, kwargs=reverse_params)
        else:
            len_response = self.client.get(reverse(route_name, kwargs=reverse_params))
            self.assertEqual(len_response.status_code, expected)
