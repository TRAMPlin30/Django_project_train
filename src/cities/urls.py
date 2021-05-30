
from django.urls import path

from cities.views import *

urlpatterns = [
    path('', cities_all, name='cities_all'),
    #path('<int:pk>/', cities_all, name='cities_all'), # отображение страници с помощью функции cities_all, которая указана в views.ру
    path('detail/<int:pk>/', CityDetailView.as_view(), name='detail'),
                             # отображение страници с помощью класса CityDetailView, который указан в views.ру
                             # класс CityDetailView отображается только с помощью функции отображения as_view (сам по себе класс не может отображаться)
                             # конструкция '<int:pk>/', говорит о том что после слеша в адресе http://127.0.0.1:8000/cities/ будет
                             # добавляться номер id города конкретного http://127.0.0.1:8000/cities/detail/1/
    path('add/', CityCreateView.as_view(), name='create'),

    path('update/<int:pk>/', CityUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', CityDeleteView.as_view(), name='delete'),

             ]

