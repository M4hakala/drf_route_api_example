from django.utils import timezone


def local_today():
    return timezone.localtime(timezone.now()).date()
