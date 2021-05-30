from django.db import models
from django.urls import reverse


class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name = 'Город')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('cities:detail', kwargs={ 'pk':(self.pk)})
        # функция get_absolute_url(self): - это функция создана для того что б данный метод
        # при создании нового объекта класса City перебрасывал нас после нажатия кнопки "Создать" "Submit"
        # на страницу с вновь созданным городом по адресу детализации каждого города - 'cities:detail' detail.html