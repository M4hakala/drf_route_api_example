from django.core.management import call_command, CommandError
from django.utils import timezone
from celery import shared_task
from io import StringIO
import datetime
from api.management.commands.calculate_longest_route import Command


@shared_task
def compute_longest_route():
    date = timezone.now().date() - datetime.timedelta(days=1)
    out = StringIO()
    try:
        call_command('calculate_longest_route', date.strftime("%Y-%m-%d"), stdout=out)
    except CommandError as e:
        raise CommandError(f'Periodic task finished with raised exception. ({e})')

    if out.getvalue().find(Command.success) < 0:
        raise CommandError(f'Periodic task finished with an error. ({out.getvalue()})')
    if out.getvalue().find(Command.warning) > -1:
        raise CommandError(f'Periodic task finished with no computations. ({out.getvalue()})')
