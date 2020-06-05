from django.contrib import admin
from api.models import CoordinatesModel, RouteModel, LongestRouteModel

admin.site.register(CoordinatesModel)
admin.site.register(RouteModel)
admin.site.register(LongestRouteModel)
