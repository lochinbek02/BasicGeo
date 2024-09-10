from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Information , MultiPointExample, MultiPoligon,MultiLineString
from django.contrib.gis.geos import Point, Polygon
import math
from django.contrib.gis.db.models.functions import Distance
from django.core.serializers import serialize
def map_view(request):
    locations = Information.objects.all()
    locations_with_distances = []

    for location in locations:
        # Calculate the distance from the current location to all other locations
        distances = Information.objects.annotate(
            distance=Distance('location', location.location)
        ).exclude(pk=location.pk).order_by('distance')
        
        locations_with_distances.append({
            'location': location,
            'distances': distances
        })

    return render(request, 'locations/map.html', {'locations_with_distances': locations_with_distances})
def location_distances(request, pk):
    selected_location = Information.objects.get(pk=pk)
    location_point = selected_location.location

    # Calculate the distance from the selected location to all other locations
    locations_with_distances = Information.objects.annotate(
        distance=Distance('location', location_point)
    ).exclude(pk=pk).order_by('distance')

    # Prepare the data to return as JSON
    data = [
        {
            'name': location.name,
            'distance': location.distance.km,
        }
        for location in locations_with_distances
    ]

    return JsonResponse(data, safe=False)

# multipoint_project/multipoint_app/views.py



def multipoint_map(request):
    points = MultiPointExample.objects.all()
    return render(request, 'multipoint_map.html', {'points': points})


def map_view_distance(request, location_id):
    selected_location = get_object_or_404(Information, id=location_id)
    
    # Radius in meters (10 km)
    radius = 10000

    # Finding locations within the 10 km radius
    nearby_locations = Information.objects.annotate(
        distance=Distance('location', selected_location.location)
    ).filter(distance__lte=radius).exclude(id=location_id)
    
    return render(request, 'locations/map_linear.html', {
        'selected_location': selected_location,
        'nearby_locations': nearby_locations,
    })
def points_polygon(request, polygon_id):
    # Get the selected polygon
    polygon = get_object_or_404(MultiPoligon, id=polygon_id)
    
    # Get points within the polygon
    points_within = MultiPointExample.objects.filter(points__contained=polygon.multipolygon)
    
    # Serialize the points to GeoJSON, including the 'name' field as a property
    points_geojson = serialize('geojson', points_within, geometry_field='points', fields=('name',))
    
    # Serialize the polygon to GeoJSON
    polygon_geojson = serialize('geojson', [polygon], geometry_field='multipolygon')

    return render(request, 'locations/points_polygon.html', {
        'polygonname': polygon,
        'polygon': polygon_geojson,
        'points': points_geojson
    })