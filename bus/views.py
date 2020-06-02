import csv

from django.core.paginator import Paginator
from django.shortcuts import render, reverse, redirect
from django.conf import settings


def pages(request):
    return redirect(f'{reverse(bus_stations)}?page=1')


def bus_stations(request):
    with open(settings.BUS_STATION_CSV, encoding='cp1251') as f:
        reader = csv.DictReader(f)
        stations_list = list(reader)
    paginator = Paginator(stations_list, 10)
    current_page = request.GET.get('page', 1)
    b_stations = paginator.get_page(current_page)
    prev_page, next_page = None, None
    if b_stations.has_previous():
        prev_page = b_stations.previous_page_number
        prev_page = prev_page()
    else:
        prev_page = 1
    if b_stations.has_next():
        next_page = b_stations.next_page_number
        next_page = next_page()
    else:
        next_page = paginator.num_pages
    return render(request, template_name='index_bus.html', context={
        'bus_stations': b_stations,
        'current_page': current_page,
        'prev_page_url': f'{reverse(bus_stations)}?page={prev_page}',
        'next_page_url': f'{reverse(bus_stations)}?page={next_page}',
    })
