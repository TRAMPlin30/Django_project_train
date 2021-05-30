from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import request
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from trains.models import Train
from trains.forms import TrainForm



__all__ = ('trains_all', 'TrainDetailView', 'TrainCreateView', 'TrainUpdateView', 'TrainDeleteView',)

#-------------------------------------------------------------------------------------------------------------------

def trains_all(request, pk = None):
    if request.method == 'POST': #если мы отправили форму, а не делаем запрос типа GET списка городов к примеру
        form = TrainForm(request.POST) #
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
    form = TrainForm(request.POST)
    all_of_trains = Train.objects.all()

#-------------------------Пагинация на основе функции (отображение объектов по странично)---------------------------------------
    lst = Paginator(all_of_trains, 3)
    page_number = request.GET.get('page')
    page_obj = lst.get_page(page_number)
    context = {'page_obj': page_obj}

#----------------------------------------------------------------
    #context = {'objects_list': all_of_cities, 'form': form}
    return render(request, 'trains/trains_all.html', context)


#__________________________________________________________________________________________________________________

class TrainDetailView(DetailView):  # DetailView - родительский класс из классов Generic display views в которм уже отображены
                                   # все функции отображения которые указываются в обычном отображении, таком как функция def cities_all(request, pk = None)
                                   # которая указана выше
    queryset = Train.objects.all()
    template_name = 'trains/detail.html'

#__________________________________________________________________________________________________________________


class TrainCreateView(SuccessMessageMixin, CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/create.html'
    success_url = reverse_lazy('trains:trains_all') # после создания города переходи на страницу (списка всех городов)
    success_message = "Поезд успешно создан!"

class TrainUpdateView(SuccessMessageMixin, UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/update.html'
    success_url = reverse_lazy('trains:trains_all') # после создания города переходи на страницу (списка всех городов)
    success_message = "Поезд успешно отредактирован!"

class TrainDeleteView(DeleteView):
    model = Train
    template_name = 'trains/delete.html'
    success_url = reverse_lazy('trains:trains_all') # после удаления города переходи на страницу (списка всех городов)


    #def get(self, request, *args, **kwargs):
        #messages.success(request, 'Город успешно удален!')
        #return self.post(request, *args, **kwargs)
