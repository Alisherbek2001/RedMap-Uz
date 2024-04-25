from django.contrib import admin
from .models import Hayvon,Osimlik,Oilasi,CoordinateHayvon,CoordinateOsimlik


class OilaAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Oilasi,OilaAdmin)

class HayvonAdmin(admin.ModelAdmin):
    list_display = ['nomi','yili','soni']
admin.site.register(Hayvon,HayvonAdmin)

class OsimlikAdmin(admin.ModelAdmin):
    list_display = ['nomi','soni']
admin.site.register(Osimlik,OsimlikAdmin)

class CoordinateHayvonAdmin(admin.ModelAdmin):
    list_display = ['nomi','x','y']
admin.site.register(CoordinateHayvon,CoordinateHayvonAdmin)

class CoordinateOsimlikAdmin(admin.ModelAdmin):
    list_display = ['nomi','x','y']
admin.site.register(CoordinateOsimlik,CoordinateOsimlikAdmin)

#o'zgarish