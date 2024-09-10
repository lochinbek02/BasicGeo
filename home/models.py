from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos import Polygon, Point
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.geos import GEOSGeometry
import json
# class User(geomodels.Model):
#     name = geomodels.CharField(max_length=100)
#     age = geomodels.PositiveIntegerField()
#     location_polygon = geomodels.PolygonField()  # Geospatial field for storing polygon (e.g., city boundaries)
#     location_point = geomodels.PointField(default=Point(69.2401, 41.2995))  # Geospatial field for storing point (e.g., city center coordinates)

#     def __str__(self):
#         return self.name


    
class Information(models.Model):
    name=models.CharField(max_length=100)
    location_name=models.CharField(max_length=200)
    location = geomodels.PointField(default=Point(69.2401, 41.2995))
    # location_polygon = geomodels.PolygonField()
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(default=timezone.now)
    updated_at=models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(Information, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('showpost',args=str(self.pk))
    
class MultiPointExample(models.Model):
    name = models.CharField(max_length=100)
    points = geomodels.MultiPointField()

    def __str__(self):
        return self.name
    @property
    def geojson(self):
        geom = GEOSGeometry(self.points)
        return geom.geojson
class MultiLineString(models.Model):
    # 2 ta nuqtani birlashtirish uchun 
    first_point_name=models.CharField(max_length=20)
    second_point_name=models.CharField(max_length=20)
    linestring=geomodels.MultiLineStringField()
    def __str__(self):
        return f"{self.first_point_name} line {self.second_point_name}"
    @property
    def geojson(self):
        geom = GEOSGeometry(self.linestring.geojson)
        return json.dumps(geom)
class MultiPoligon(models.Model):
    polygon_name = models.CharField(max_length=100)
    multipolygon = geomodels.MultiPolygonField()

    def __str__(self):
        return self.polygon_name
    
    @property
    def geojson(self):
        geom = GEOSGeometry(self.multipolygon.geojson)
        return geom.json


