from django.db import models
from core import utils


class RouteModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    local_date = models.DateField(default=utils.local_today)
    distance = models.FloatField(default=0)

    class Meta:
        db_table = 'route_routes'

    def __str__(self):
        return "route_#{}_distance:{}_local_date:{}".format(self.id, self.distance, self.local_date)

    @property
    def route_id(self):
        return self.id
