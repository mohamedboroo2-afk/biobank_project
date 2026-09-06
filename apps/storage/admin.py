from django.contrib import admin
from .models import Facility, Room, Freezer, Rack, Box, StorageLocation

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'address', 'is_active')
    search_fields = ('code', 'name')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'facility', 'is_active')
    search_fields = ('code', 'name')
    list_filter = ('facility', 'is_active')

@admin.register(Freezer)
class FreezerAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'room', 'freezer_type', 'temperature', 'is_active')
    list_filter = ('freezer_type', 'is_active', 'room__facility')
    search_fields = ('code', 'name')

@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'freezer', 'rows', 'columns', 'is_active')
    search_fields = ('code', 'name')
    list_filter = ('is_active',)

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'rack', 'box_type', 'rows', 'columns', 'is_full', 'is_active')
    search_fields = ('code', 'name')
    list_filter = ('box_type', 'is_full', 'is_active')

@admin.register(StorageLocation)
class StorageLocationAdmin(admin.ModelAdmin):
    list_display = ('box', 'row', 'column', 'is_occupied')
    list_filter = ('is_occupied',)
    search_fields = ('box__code',)