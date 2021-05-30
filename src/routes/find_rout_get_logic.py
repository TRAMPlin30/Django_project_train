from trains.models import Train

#-----------------------------------------------------------------------------------------------------------------
def dfs_path(graf, start, goal):
    '''
    Функция поиска всех возможных маршрутов
    из одного города в другой. Вариант посещения
    одного и того же города не рассматривается
    Данная функция взята из стековерфлоу как один из возможных
    вариантов реализации решения алгоритма поиска DFS
    Depth-first seach (DFS) code in python
    https://stackoverflow.com/questions/43430309/depth-first-search-dfs-code-in-python
    '''
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graf.keys():
            for next_ in graf[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))
#------------------------------------------------------------------------------------------------------------------


def get_graf(qs):
    graf = {}
    for q in qs:
        graf.setdefault(q.from_city_id, set())
        graf[q.from_city_id].add(q.to_city_id)
    return graf


def get_routes(request, form) -> dict:
    context = {'form':form}
    qs = Train.objects.all()
    graf = get_graf(qs)
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    cities = data['cities']
    traveling_time = data['travel_time']
    all_ways = list(dfs_path(graf, from_city.id, to_city.id))
    if not len(all_ways):
        raise ValueError('Маршрута, удовлетворяющего условия не существует')

    if cities:
        _cities = [city.id for city in cities]
        right_ways = []
        for rout in all_ways:
            if all(city in rout for city in _cities): # функция qwery_set
                right_ways.append(rout)
        if not right_ways:
            raise ValueError('Маршрут через эти города не возможен')
    else:
        right_ways = all_ways
    routes = []
    all_trains = {}
    for q in qs:
        all_trains.setdefault((q.from_city_id, q.to_city_id), [])
        all_trains[(q.from_city_id, q.to_city_id)].append(q)
    for rout in right_ways:
        tmp = {}
        tmp['trains'] = []
        total_time = 0
        for i in range (len(rout) - 1):
            qs = all_trains[(rout[i], rout[i+1])]
            q = qs[0]
            total_time += q.travel_time
            tmp['trains'].append(q)
        tmp['total_time'] = total_time
        if total_time <= traveling_time:
            # если общее время в пути меньше заданного
            # то добавляем маршрут в общий список
            routes.append(tmp)
    if not routes:
        # если список пуст, то нет таких маршрутов
        # которые бы удовлетворяли заданным параметрам
        raise ValueError('Время в пути не соответствует заданному')

    sorted_routes = []
    if len(routes) == 1:
        sorted_routes = routes
    else:
        times = list(set(r['total_time'] for r in routes))
        times = sorted(times)
        for time in times:
            for route in routes:
                if time == route['total_time']:
                    sorted_routes.append(route)
    context['routes'] = sorted_routes
    context['cities'] = {'from_city': from_city, 'to_city': to_city}

    return context

