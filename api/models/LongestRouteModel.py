from django.db import models
from api.models import RouteModel


class LongestRouteModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    route_date = models.DateField(unique=True)
    route = models.OneToOneField(
        RouteModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    class Meta:
        db_table = 'route_longest_route'

    def __str__(self):
        return "route_#{}_distance:{}_date:{}".format(self.route.route_id, self.route.distance, self.route_date)
