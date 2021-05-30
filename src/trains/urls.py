
from django.urls import path

from trains.views import *

urlpatterns = [
    path('', trains_all, name='trains_all'),

    path('detail/<int:pk>/', TrainDetailView.as_view(), name='detail'),

    path('add/', TrainCreateView.as_view(), name='create'),

    path('update/<int:pk>/', TrainUpdateView.as_view(), name='update'),

    path('delete/<int:pk>/', TrainDeleteView.as_view(), name='delete'),

             ]

