from django.contrib import admin
from .models import Sensor,Unit, measurement, user_sensor

class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'key')

class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')

class MeasAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'value', 'unit', 'date')

class UserSensorAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')

# Register your models here.
admin.site.register(Sensor, SensorAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(measurement, MeasAdmin)
admin.site.register(user_sensor, UserSensorAdmin)
