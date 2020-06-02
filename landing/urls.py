from django.urls import path

from app.views import landing, stats, index
from bus.views import pages, bus_stations


urlpatterns = [
    path('', index, name='index'),
    path('landing/', landing, name='landing'),
    path('stats/', stats, name='stats'),
    path('pages/', pages, name='pages'),
    path('bus_stations/', bus_stations, name='bus_stations'),
]