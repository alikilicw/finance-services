from collections import OrderedDict
from .get_stock_price import get_stock_price
from .driver import get_driver

def convert_price_to_float(value: str) -> float:

    try:
        value_ = float(value.replace(',', ''))
    except:
        pass

    return value_

def fix_financial_data(data: dict) -> dict:
    
    fin_tables = dict(data['financial_tables'])

    _0 = list(fin_tables.keys())[0]
    _1 = list(fin_tables.keys())[1]
    _2 = list(fin_tables.keys())[2]
    _3 = list(fin_tables.keys())[3]

    for period, value in fin_tables.items():
        for kalem, value in dict(value).items():
            fin_tables[period][kalem] = float(str(value).replace('.', ''))

    if str(_3).split('/')[1] != '3': 

        fin_tables[_3]['donem_kari_(zarari)'] = fin_tables[_3]['donem_kari_(zarari)'] - fin_tables[_2]['donem_kari_(zarari)']
        fin_tables[_3]['brut_kar_(zarar)'] = fin_tables[_3]['brut_kar_(zarar)'] - fin_tables[_2]['brut_kar_(zarar)']

    if str(_2).split('/')[1] != '3':

        fin_tables[_2]['donem_kari_(zarari)'] = fin_tables[_2]['donem_kari_(zarari)'] - fin_tables[_1]['donem_kari_(zarari)']
        fin_tables[_2]['brut_kar_(zarar)'] = float(fin_tables[_2]['brut_kar_(zarar)']) - fin_tables[_1]['brut_kar_(zarar)']

    if str(_1).split('/')[1] != '3':

        fin_tables[_1]['donem_kari_(zarari)'] = fin_tables[_1]['donem_kari_(zarari)'] - fin_tables[_0]['donem_kari_(zarari)']
        fin_tables[_1]['brut_kar_(zarar)'] = fin_tables[_1]['brut_kar_(zarar)'] - fin_tables[_0]['brut_kar_(zarar)']

    del data['financial_tables'][list(dict(data['financial_tables']).keys())[0]]
    for Key, Value in dict(data['financial_tables']).items():
        data[Key] = dict(Value)
    del data['financial_tables']

    
    P = OrderedDict() #her bir şirket için nihai dict oluştur

    P['stock_code'] = data['stock_code']

    driver = get_driver()

    periods = []
    for index, key in enumerate(list(dict(data).keys())): #dönemleri sırala
        if index < 1: continue # ilki dönem değil, onunla işlem yapma
        kalemler = dict(data[key])
        periods.append(key)

        key = str(key)
        stock_code = data['stock_code']

        if index == 1:
            P['first_period_price'] = convert_price_to_float(get_stock_price(key.split('/')[1], key.split('/')[0], stock_code, driver))

            for kalem, value in kalemler.items():
                P[f'first_period_{kalem}'] = value

        if index == 2:
            P['second_period_price'] = convert_price_to_float(get_stock_price(key.split('/')[1], key.split('/')[0], stock_code, driver))

            for kalem, value in kalemler.items():
                P[f'second_period_{kalem}'] = value
        if index == 3:
            P['third_period_price'] = convert_price_to_float(get_stock_price(key.split('/')[1], key.split('/')[0], stock_code, driver))

            for kalem, value in kalemler.items():
                P[f'third_period_{kalem}'] = value
    
    
    P['periods'] = periods
    driver.quit()
    return P