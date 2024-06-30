from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotFound
from .models import DATABASE
from django.http import HttpResponse
from logic.services import filtering_category
from logic.services import view_in_cart, add_to_cart, remove_from_cart
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
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
        return render(request,
                      'store/shop.html',
                      context={"products": DATABASE.values()})

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
@login_required(login_url='login:login_view')
def cart_view(request):
    if request.method == 'GET':
        current_user = get_user(request).username
        data = view_in_cart(request)[current_user]
        if request.GET.get('format') == 'JSON':
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})
        products = []
        for product_id, quantity in data['products'].items():
            product = DATABASE[product_id]
            product['quantity'] = quantity
            product['price_total'] = f"{quantity * product['price_after']:.2f}"
            products.append(product)

        return render(request, 'store/cart.html', context={'products':products})

@login_required(login_url='login:login_view')
def cart_add_view(request, id_product):
    if request.method == 'GET':
        result = add_to_cart(request, id_product)
        if result:
            return JsonResponse({'answer':'Продукт успешно добавлен в корзину'},
                                json_dumps_params={'ensure_ascii': False})
        return JsonResponse({'answer': 'Неудачное добавление в корзину'},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

def cart_del_view(request, id_product):
    if request.method == 'GET':
        result = remove_from_cart(request, id_product)
        if result:
            return JsonResponse({'answer':'Продукт успешно удален из корзины'},
                                json_dumps_params={'ensure_ascii': False})
        return JsonResponse({'answer': 'Неудачное удаление из корзины'},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})
def coupon_check_view(request, name_coupon):
    DATA_COUPON = {
        "coupon": {
            "value": 10,
            "is_valid": True},
        "coupon_old": {
            "value": 20,
            "is_valid": False},
        }
    if request.method == "GET":
        if name_coupon in DATA_COUPON:
            return JsonResponse({'discount': DATA_COUPON[name_coupon]["value"], 'is_valid': DATA_COUPON[name_coupon]["is_valid"]},
                                json_dumps_params={'ensure_ascii': False})
        return HttpResponseNotFound("Неверный купон")
def delivary_estimate_view(request):
    DATA_PRICE = {
        "Россия": {
            "Москва": {"price": 80},
            "Санкт-Петербург": {"price": 80},
            "fix_price": 100,
        }
    }
    if request.method == "GET":
        data = request.GET
        country = data.get('country')
        city = data.get('city')
        if country and city in DATA_PRICE[country]:
            return JsonResponse({"price": DATA_PRICE[country][city]["price"]},
                                json_dumps_params={'ensure_ascii': False})
        elif country in DATA_PRICE and city not in DATA_PRICE[country]:
            return JsonResponse({"price": DATA_PRICE[country]["fix_price"]},
                                json_dumps_params={'ensure_ascii': False})
        elif country not in DATA_PRICE:
            return HttpResponse("Неверные данные")

@login_required(login_url='login:login_view')
def cart_buy_now_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(request, id_product)
        if result:
            return redirect("store:cart_view")

        return HttpResponseNotFound('Неудачное добавление в корзину')
def cart_remove_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(request, id_product)
        if result:
            return redirect("store:cart_view")

        return HttpResponseNotFound("Неудачное удаление из корзины")



