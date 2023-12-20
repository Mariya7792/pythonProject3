from django.http import HttpResponse
from datetime import datetime
# Create your views here.

def datetime_view(request):
    if request.method == 'GET':
        data = datetime.now()
        return HttpResponse(data)
