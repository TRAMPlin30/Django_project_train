from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import request
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from cities.models import City
from cities.forms import HtmlForm, CityForm


__all__ = ('cities_all', 'CityDetailView', 'CityCreateView', 'CityUpdateView', 'CityDeleteView')

#-------------------------------------------------------------------------------------------------------------------

def cities_all(request, pk = None):
    if request.method == 'POST': #если мы отправили форму, а не делаем запрос типа GET списка городов к примеру
        form = CityForm(request.POST) #
        if form.is_valid():
            print(form.cleaned_data)
            form.save()

        #if pk: # если какоето значение pk (id) пришло из вне, то делаем запрос к базе данных что б его отобразить
        #city = City.objects.filter(id=pk).first() - методы QuerySet
        #city = get_object_or_404(City, id=pk) # pk это тоже самое что и id в Djange (id принимает значение запроса pk
        #context = {'object': city}
        #return render(request, 'cities/detail.html', context)
    form = CityForm(request.POST)
    all_of_cities = City.objects.all()

#-------------------------Пагинация на основе функции (отображение объектов по странично)---------------------------------------
    lst = Paginator(all_of_cities, 3)
    page_number = request.GET.get('page')
    page_obj = lst.get_page(page_number)
    context = {'page_obj': page_obj, 'form': form}

#----------------------------------------------------------------
    #context = {'objects_list': all_of_cities, 'form': form}
    return render(request, 'cities/cities_all.html', context)


#__________________________________________________________________________________________________________________

class CityDetailView(DetailView): # DetailView - родительский класс из классов Generic display views в которм уже отображены
                                  # все функции отображения которые указываются в обычном отображении, таком как функция def cities_all(request, pk = None)
                                  # которая указана выше
    queryset = City.objects.all() #
    template_name = 'cities/detail.html'


class CityCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    # LoginRequiredMixin - django-mixin, обработан в приложении accounts (будет срабатывать
    # перед вызовом функции в которой он указан как аргумент

    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('cities:cities_all') # после создания города переходи на страницу (списка всех городов)
    success_message = "Город успешно создан!"

class CityUpdateView(SuccessMessageMixin, UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    success_url = reverse_lazy('cities:cities_all') # после создания города переходи на страницу (списка всех городов)
    success_message = "Город успешно отредактирован!"


class CityDeleteView(DeleteView):
    model = City
    template_name = 'cities/delete.html'
    success_url = reverse_lazy('cities:cities_all') # после удаления города переходи на страницу (списка всех городов)

    #def get(self, request, *args, **kwargs):
        #messages.success(request, 'Город успешно удален!')
        #return self.post(request, *args, **kwargs)
