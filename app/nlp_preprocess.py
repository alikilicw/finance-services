from .utils import Utilities

def preprocess(news, stock_codes_new, utilities: Utilities, nlp) -> dict:

    output = dict()
    output['stock_code'] = news['stock_code']
    output['periods'] = news['periods']

    #'item' sözlüğündeki anahtar ve değerler üzerinde döngüye girilir.
    for key, value in dict(news).items():

        #Anahtar 'stock_code' ise bu anahtarı işleme almıyoruz, sadece haber içeriğini işliyoruz.
        if key != 'stock_code' and key != 'periods':

            if key not in output:
                output[key] = list()

            # Her bir haber içeriği için aşağıdaki işlemler yapılır.
            for haber in value:
                haber = str(haber)
                #Eğer haber boşsa, işlem yapılmaz ve bir sonraki habere geçilir.
                if len(haber) == 0:
                    continue

                hedef_dil = "en"  # Çevirilecek hedef dil
                try:
                    haber = utilities.cevir(haber, hedef_dil) # Metni çevirir
                except Exception as err:
                    print(err, 'TRANSLATE ERROR')
                    continue
                
                #Haberi cümlelere ayırır.
                sentences = utilities.cumlelere_ayir(nlp, haber)
                del sentences[-8:] #Her haber sayfasının son 8 cümlesi gereksiz.

                #Yeni cümleler için boş bir liste oluşturulur.
                haber_ = list()

                # Her bir cümle üzerinde döngüye girilir
                for sentence in sentences:
                    sentence = str(sentence)
                    #Cümlenin uzunluğu 4999'dan (translator max length) büyükse veya boşsa, işlem yapılmaz.
                    if len(sentence) > 4999 or len(sentence) < 40 :
                        continue    

                    temiz_cumle = sentence

                    #Cümle içerisinde hisse kodunu ara
                    cumle_okay = True
                    for stock_code in stock_codes_new:
                        if stock_code == news["stock_code"]:
                            continue
                        if temiz_cumle.find(stock_code) != -1:
                            cumle_okay= False
                            break
                    
                    #Cümle farklı hisselerin kodlarını içermiyorsa işlem yapılır.
                    if cumle_okay and len(temiz_cumle) > 70:
                        
                        temiz_cumle = utilities.clean_text(temiz_cumle)

                        # Durak kelimeleri (stop words) kaldır.
                        temiz_cumle = utilities.remove_stop_words(nlp, temiz_cumle)

                        haber_.append(temiz_cumle)


                output[key] = haber_

    return output