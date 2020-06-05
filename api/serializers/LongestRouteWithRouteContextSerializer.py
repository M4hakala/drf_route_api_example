from rest_framework import serializers
from api.models import LongestRouteModel, RouteModel


class LongestRouteWithRouteContextSerializer(serializers.ModelSerializer):
    def __init__(self, route: RouteModel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.route = route

    class Meta:
        model = LongestRouteModel
        fields = ('route_date',)

    def create(self, validated_data):
        longest_route = LongestRouteModel.objects.create(route=self.route, **validated_data)

        return longest_route
