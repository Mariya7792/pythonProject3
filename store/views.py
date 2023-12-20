from django.shortcuts import render
from django.http import JsonResponse
from .models import DATABASE
# Create your views here.

def products_view(request):
    if request.method == 'GET':
        return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})
