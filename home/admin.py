from django.contrib import admin

from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Information , MultiPointExample, MultiLineString, MultiPoligon


# admin.site.register(User, LeafletGeoAdmin)

    
admin.site.register(Information,LeafletGeoAdmin)
class MultiPointExampleAdmin(LeafletGeoAdmin):
    list_display = ('name', 'points')
class MultiLineStringExampleAdmin(LeafletGeoAdmin):
    list_display = ('first_point_name', 'second_point_name','linestring')
class MultiPoligonExampleAdmin(LeafletGeoAdmin):
    list_display = ('polygon_name', 'multipolygon')
admin.site.register(MultiPointExample, MultiPointExampleAdmin)
admin.site.register(MultiLineString, MultiLineStringExampleAdmin)
admin.site.register(MultiPoligon, MultiPoligonExampleAdmin)

