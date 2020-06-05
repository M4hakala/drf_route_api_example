from django.core.management import call_command, CommandError
from django.utils import timezone
from django.test import TestCase
from api.tests.utils.route_functions import create_route_with_coordinates
from io import StringIO
from parameterized import parameterized


class CalculateLongestRouteCommandTestCase(TestCase):
    def test_successful_process(self):
        date = timezone.now().date()
        _ = create_route_with_coordinates([
            {"lat": -25.4025905, "lon": -49.3124416},
            {"lat": -23.559798, "lon": -46.634971},
        ])

        out = StringIO()
        call_command('calculate_longest_route', date.strftime("%Y-%m-%d"), stdout=out)
        self.assertIn('Longest route successfully calculated for', out.getvalue())

    @parameterized.expand([
        ('2020-02-a1',),
        ('20200201',),
        ('2020-22-01',),
    ])
    def test_invalid_parameters(self, param):
        with self.assertRaises(CommandError) as e:
            call_command('calculate_longest_route', param)
        self.assertEqual('Invalid date parameter.', str(e.exception))

    def test_without_parameters(self):
        with self.assertRaises(CommandError) as e:
            call_command('calculate_longest_route')
        self.assertEqual('Error: the following arguments are required: date', str(e.exception))

    def test_no_routes_found(self):
        out = StringIO()
        call_command('calculate_longest_route', '2020-01-01', stdout=out)
        self.assertIn('No routes found for date', out.getvalue())
