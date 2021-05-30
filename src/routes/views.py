from django.contrib import messages
from django.shortcuts import render, redirect


# Create your views here.
from django.views.generic import ListView

from cities.models import City
from routes.find_rout_get_logic import get_routes
from routes.forms import RouteForm, RouteModelForm
from routes.models import Route
from trains.models import Train


def routes_all(request):
    form = RouteForm()
    return render(request, 'routes/routes_all.html', {'form':form})


def find_routes(request): # функция отображения формы (поссле передачи в нее данных
    if request.method == "POST":
        form = RouteForm(request.POST)
# ------------------------------------------------------------------------------------------------------------
        #когда браузер передаст данные от пользователя из формы методом POST, мы проверяем эти данные на валидность
        if form.is_valid(): #если форма валидна, то
            try: # пробуем получить данные из функции get_routes исходя из тех параметров которые мы внее отправили
                 # и ожидаем от нее получить некий список маршрутов context (если найдены маршруты)
                context = get_routes(request, form)
                # отображаем context (*)-  return render(request, 'routes/routes_all.html', context)
#------------------------------------------------------------------------------------------------------------
            except ValueError as e: # если маршрутов с соответствующими требованиями нет, то вернем собщение "е"
                                    # которое покажем пользователю
                messages.error(request, e)
                return render(request, 'routes/routes_all.html', {'form': form}) # и вернемся опять на форму ввода данных
# ------------------------------------------------------------------------------------------------------------
            return render(request, 'routes/routes_all.html', context) # коментарий выше (*)
# ------------------------------------------------------------------------------------------------------------
        return render(request, 'routes/routes_all.html', {'form': form})
        # если форма не валидна, то возвращаемся на страницу ввода данных в форму и сама по себе форма
        # укажет пользователю те места на которые нужно будет обратить внимание, какие данные не валидны
# ------------------------------------------------------------------------------------------------------------
    else:
        form = RouteForm()
        messages.error(request, 'Нет данных для поиска')
        return render(request, 'routes/routes_all.html', {'form': form})



# ------------------------------------------------------------------------------------------------------------
def add_route(request):
    if request.method == "POST":
        context = {}
        data = request.POST
        if data: # вытаскиваем данные которые поступили из формы hidden в переменную data = request.POST
        #-------------------------------------------------------------------------------------------------------
            total_time =int(data['total_time']) # забрали данные
            from_city_id = int(data['from_city']) # забрали данные
            to_city_id = int(data['to_city']) # забрали данные
            trains = data['trains'].split(',') # забрали данные
            # обрабатываем эти данные
            trains_list = [int(t) for t in trains if t.isdigit()]  # проверка данных на соответствие (нахуя? х.з.)
            # получаем набор поездов (екземпляры)
            qs = Train.objects.filter(id__in= trains_list).select_related('from_city', 'to_city')
            cities = City.objects.filter(id__in=[from_city_id, to_city_id]).in_bulk()
        # когда данные собрали, ими нужно наполнить форму django (class RouteModelForm(forms.ModelForm)
            form = RouteModelForm(initial={
                                            'from_city': cities[from_city_id], # скрытое поле, которое заполняется данными из переменной data (data = request.POST)
                                            'to_city': cities[to_city_id], # скрытое поле, которое заполняется данными из переменной data (data = request.POST)
                                            'travel_time': total_time, # скрытое поле, которое заполняется данными из переменной data (data = request.POST)
                                            'trains': qs }                     ) # скрытое поле, которое заполняется данными из переменной data (data = request.POST)
        # пробрасываем данные в шаблон для отрисовки
            context['form'] = form
        return render(request, 'routes/save_route.html', context )
    else:
        messages.error(request, 'Нет данных для сохранения (маршрут отсутствует)')
        return redirect('/') # перенаправляемся на главную страницу


def save_route(request):
    if request.method == "POST":
        form = RouteModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Маршрут успешно сохранен!")
            return redirect('/')
        return render(request, 'routes/save_route.html', {'form':form} )
    else:
        messages.error(request, 'Нет данных для сохранения (маршрут отсутствует)')
        return redirect('/') # перенаправляемся на главную страницу


class RouteListView(ListView):
    paginate_by = 10
    model = Route
    template_name = 'routes/list.html'
