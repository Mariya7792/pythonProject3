from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from app_weather.weather_api import current_weather
# Create your views here.
def my_view(request):
    lat = '59.93'
    lon = '30.31'
    if request.method == 'GET':
        data = current_weather(lat, lon)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})