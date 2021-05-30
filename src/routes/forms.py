from django import forms

from cities.models import City
from routes.models import Route
from trains.models import Train


class RouteForm(forms.Form):

    from_city = forms.ModelChoiceField(label='Откуда:',
                                       queryset=City.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control', }))

    to_city = forms.ModelChoiceField(label='Куда:',
                                     queryset=City.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control', }))



    cities = forms.ModelMultipleChoiceField(label='Через города:  ( нажмите "Сtrl" для выбора нескольких городов )', queryset=City.objects.all(),
                                            required=False, widget=forms.SelectMultiple(attrs={'class': 'form-control',}))

    travel_time = forms.IntegerField(label='Время в пути',
                                     widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'Введите время в пути'}))



class RouteModelForm(forms.ModelForm):
    name = forms.CharField(label='Введите название маршрута',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'Введите название маршрута'}))
    from_city = forms.ModelChoiceField(queryset=City.objects.all(),widget=forms.HiddenInput(),)
    to_city = forms.ModelChoiceField(queryset=City.objects.all(),widget=forms.HiddenInput(),)
    trains = forms.ModelMultipleChoiceField( queryset=Train.objects.all(),
                                             required=False,
                                             widget=forms.SelectMultiple(attrs={'class': 'form-control d-none',}))
    travel_time = forms.IntegerField(widget=forms.HiddenInput(),)

    class Meta:
        model = Route
        fields = '__all__'