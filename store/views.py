from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from .models import DATABASE
from django.http import HttpResponse
from logic.services import filtering_category
# Create your views here.

def products_view(request):
    if request.method == 'GET':
        # id = request.GET.get('id')
        NOTFOUND = 'HttpResponseNotFound ("Данного продукта нет в базе данных")'
        # if id:
        #     if id in DATABASE:
        #         return JsonResponse(DATABASE[id], json_dumps_params={'ensure_ascii': False,
        #                                                          'indent': 4})
        #     else:
        #         return JsonResponse(NOTFOUND, json_dumps_params={'ensure_ascii': False,
        #                                                          'indent': 4}, safe=False)
        # else:
        #     return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False,
        #                                                  'indent': 4})
        if id_product := request.GET.get('id'):
            if data := DATABASE.get(id_product):
                return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                             'indent': 4})
            return HttpResponseNotFound('Данного продукта нет в базе данных')

        category_key = request.GET.get('category')
        if ordering_key := request.GET.get('ordering'):
            if str(request.GET.get('reverse')).lower() == 'true':
                data = filtering_category(DATABASE, category_key, ordering_key, reverse=True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key, reverse=False)
        else:
            data = filtering_category(DATABASE, category_key)

        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii' : False,
                                                                 'indent':4})
def shop_view(request):
    if request.method == 'GET':
        with open('store/shop.html', encoding='utf-8') as f:
            data = f.read()
        return HttpResponse(data)

def products_page_view(request, page):
    if request.method == 'GET':
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:
                    with open(f'store/products/{page}.html', encoding='utf-8') as f:
                        data = f.read()
                    return HttpResponse(data)
        elif isinstance(page, int):
            data = DATABASE.get(str(page))
            if data:
                with open(f'store/products/{data["html"]}.html', encoding='utf-8') as f:
                    data = f.read()
                return HttpResponse(data)

        return HttpResponse(status=404)