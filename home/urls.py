from django.urls import path
from . import views

urlpatterns = [
    path('map/', views.map_view, name='map_view'),
    path('location-distances/<int:pk>/', views.location_distances, name='location_distances'),
    path('multipoint/', views.multipoint_map),
    path('map/<int:location_id>/', views.map_view_distance ),
     path('polygon/<int:polygon_id>/points/', views.points_polygon, name='points_polygon'),

]
