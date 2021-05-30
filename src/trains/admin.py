from django.contrib import admin

# Register your models here.

from trains.models import Train



#-------------------изменяем поля, которые будем видеть в админке------------------------------
class TrainAdmin(admin.ModelAdmin):
    class Meta:
        model = Train
    list_display = ('name', 'from_city', 'to_city', 'travel_time')
    list_editable = ('travel_time',)
#-------------------изменяем поля, которые будем видеть в админке------------------------------



admin.site.register(Train, TrainAdmin)
