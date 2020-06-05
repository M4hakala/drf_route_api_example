from api import views
from django.urls import path, re_path

app_name = 'api'

URL_NAMES = {
    'route.get_longest_route': 'get-longest-route',
    'route.route_create': 'route-create',
    'route.route_get_length': 'route-get-length',
    'route.route_add_way_point': 'route-add-way-point',
}

urlpatterns = [
    re_path(
        r'^distance/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/longest/$',
        views.DistanceApiView.as_view(),
        name=URL_NAMES['route.get_longest_route']
    ),
    path('', views.CreateRouteApiView.as_view(), name=URL_NAMES['route.route_create']),
    path('<int:pk>/length/', views.DetailRouteApiView.as_view(), name=URL_NAMES['route.route_get_length']),
    path('<int:pk>/way_point/', views.RouteWayPointApiView.as_view(), name=URL_NAMES['route.route_add_way_point']),
]
