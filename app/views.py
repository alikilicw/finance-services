from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .scrape_tools.financial_tables import get_financial_tables
from .scrape_tools.final import fix_financial_data
from .scrape_tools.news import news
import json

def deneme(request):

    stock_code = request.GET.get('stock_code')

    # print(get_financial_tables(stock_code))

    # print(fix_financial_data((get_financial_tables(stock_code))))

    values = get_financial_tables(stock_code)


    # FileManager('a.json').write_json(fix_financial_data(values))


    # return JsonResponse({request.GET.get('stock_code'): values})
    return JsonResponse({request.GET.get('stock_code'): fix_financial_data(values)})

financial_data = dict()

def get_financial_tables_(request):
    stock_code = request.GET.get('stock_code')

    values = get_financial_tables(stock_code)
    values_ = fix_financial_data(values)

    return JsonResponse(values_, safe=False)

@csrf_exempt
def get_news(request):
    body = request.body
    body_ = body.decode('utf-8')
    stock_data = json.loads(body_)

    value = news(stock_data)
    print(value)
    return JsonResponse(value)