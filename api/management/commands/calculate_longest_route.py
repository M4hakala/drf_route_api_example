from django.core.management.base import BaseCommand, CommandError
from api import utils
import datetime


class Command(BaseCommand):
    help = 'Calculating longest route for given day'
    success = 'Longest route successfully calculated for'
    warning = 'No routes found for date'

    def add_arguments(self, parser):
        parser.add_argument('date', type=str, help="Date of longest route calculation in Y-m-d format.")

    def handle(self, *args, **options):
        try:
            route_date = datetime.datetime.strptime(options['date'], "%Y-%m-%d").date()
        except ValueError:
            raise CommandError("Invalid date parameter.")

        route = utils.find_longest_route(route_date)
        if route:
            self.stdout.write(self.style.SUCCESS(f'{self.success} {route_date}'))
        else:
            self.stdout.write(self.style.WARNING(f'{self.warning} {route_date}.'))
