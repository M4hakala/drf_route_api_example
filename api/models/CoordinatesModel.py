from django.db import models
from api import models as api_models


class CoordinatesModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lat = models.DecimalField(max_digits=10, decimal_places=8)
    lon = models.DecimalField(max_digits=11, decimal_places=8)
    route = models.ForeignKey(api_models.RouteModel, on_delete=models.CASCADE, related_name='coordinates')

    class Meta:
        db_table = 'route_coordinates'
        ordering = ['created_at']

    def __str__(self):
        return "route_#{}_lat_{}_lon_{}".format(self.route.route_id, self.lat, self.lon)
