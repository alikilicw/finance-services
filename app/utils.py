import re, string, requests
from googletrans import Translator
from core.settings import API_URL, headers

class Utilities:

  # Metinden sayıları kaldıran fonksiyon
  def metinden_sayilari_sil(self, metin):
    temiz_metin = re.sub(r'\d+', '', metin)
    return temiz_metin

  # Google Translate API'ı kullanarak Türkçe metni İngilizce'ye çevirme
  def cevir(self, metin, hedef_dil="en"):
    translator = Translator()
    cevrilmis_metin = translator.translate(metin, dest=hedef_dil).text
    return cevrilmis_metin

  def remove_stop_words(self, nlp, text):
    doc = nlp(text)
    no_stop_words = [token.text for token in doc if not token.is_stop]
    return " ".join(no_stop_words)

  def clean_text(self, text):
    temiz_cumle = re.sub(r'['+string.punctuation+']', '', text)  # Noktalama işaretlerini kaldırır
    temiz_cumle = re.sub(r'[^\w\s]', '', temiz_cumle)  # Emojiler dahil, kelime karakterleri ve boşluklar dışındakileri kaldırır
    temiz_cumle = temiz_cumle.strip()
    temiz_cumle = self.metinden_sayilari_sil(temiz_cumle)
    temiz_cumle = temiz_cumle.replace('\n', '').replace('Source', '')
    return temiz_cumle
  
  def text_model(self, payload):
    response = requests.post(API_URL, headers=headers, json=payload)

    output = 0
    for item in response.json()[0]:
      if item['label'] == 'positive':
        output = item['score']
        print(item)

    return output
  
  def cumlelere_ayir(self, nlp, text):
    doc = nlp(text)
    
    sents = []
    for sent in doc.sents:
      sents.append(sent.text)

    return sents