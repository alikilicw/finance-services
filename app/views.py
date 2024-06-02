from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import Utilities
from core.file_manager import FileManager
import json, spacy, pandas as pd, pickle
from .nlp_preprocess import preprocess
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor

utilities = Utilities()
nlp = spacy.load("en_core_web_sm")
stock_codes_new = FileManager('stock_codes_new.json').read_from_json()

@csrf_exempt
def nlp_view(request):
    body = request.body
    body_ = body.decode('utf-8')
    news_ = json.loads(body_)

    news = news_['news']

    stock_dict = {}  #Her bir hisse kodu için bir sözlük oluşturulur.

    preprocessed_data = preprocess(news, stock_codes_new, utilities, nlp)

    FileManager('preprocessed.json').write_to_json(preprocessed_data)
    
    stock_dict['stock_code'] = preprocessed_data['stock_code'] #Hisse kodunu sözlüğe eklenir.

    #Eğer 'first_period' anahtarı 'stock_dict' sözlüğünde yoksa, varsayılan değeri 5 olarak ayarlanır.
    if 'first_period_news_value' not in stock_dict:
        stock_dict['first_period_news_value'] = .5

    if 'second_period_news_value' not in stock_dict:
        stock_dict['second_period_news_value'] = .5

    if 'third_period_news_value' not in stock_dict:
        stock_dict['third_period_news_value'] = .5

    #sözlükteki anahtar ve değerler üzerinde döngüye girilir.
    for key, value in dict(preprocessed_data).items():

        #Anahtar 'stock_code' ise bu anahtarı işleme almıyoruz, sadece haber içeriğini işliyoruz.
        if key != 'stock_code' and key != 'periods':

            positive_values_sum = 0
            valid_cumle_sayisi = 0

            # Her bir haber içeriği için aşağıdaki işlemler yapılır.
            for haber in value:

                try:
                    haber = str(haber)
                    # print(haber)

                    a = utilities.text_model(haber)

                    positive_values_sum += a
                    valid_cumle_sayisi += 1

                    print('---------------------------')
                    print()

                    if valid_cumle_sayisi > 0:
                        stock_positive_values_average = positive_values_sum / valid_cumle_sayisi
                        print(stock_positive_values_average)

                        print(positive_values_sum, 'positif degerler toplami')
                        print(valid_cumle_sayisi, 'valid cumler sayisi')

                        # Eğer anahtar 'first_period' ise, hissenin pozitif değerler ortalamasını güncelle.
                        if key == 'first_period':
                            stock_dict['first_period_news_value'] = stock_positive_values_average
                        if key == 'second_period':
                            stock_dict['second_period_news_value'] = stock_positive_values_average
                        if key == 'third_period':
                            stock_dict['third_period_news_value'] = stock_positive_values_average
                except:
                    pass

    return JsonResponse(stock_dict)


@csrf_exempt
def ai_view(request):
    body = request.body
    body_ = body.decode('utf-8')
    data_ = json.loads(body_)

    data = data_['data']

    df = pd.DataFrame(data)

    loaded_scaler = FileManager('scaler.pkl').read_from_pkl()
    loaded_model = FileManager('mlp_regressor_model.pkl').read_from_pkl()

    X = df[['first_period_price', 'first_period_toplam_varliklar', 'first_period_toplam_ozkaynaklar',
            'first_period_brut_kar_(zarar)', 'first_period_donem_kari_(zarari)',
            'second_period_price', 'second_period_toplam_varliklar', 'second_period_toplam_ozkaynaklar',
            'second_period_brut_kar_(zarar)', 'second_period_donem_kari_(zarari)',
            'third_period_price', 'third_period_toplam_varliklar', 'third_period_toplam_ozkaynaklar',
            'third_period_brut_kar_(zarar)', 'third_period_donem_kari_(zarari)',
            'first_period_news_value', 'second_period_news_value', 'third_period_news_value']].values
    
    data_ = loaded_scaler.transform(X)

    prediction = loaded_model.predict(data_)

    result = {
        'prediction': prediction[0]
    }

    print(result)


    return JsonResponse(result)