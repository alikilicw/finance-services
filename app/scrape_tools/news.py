from .driver import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.utils.file_manager import FileManager


#Haberlerden aylar isimle geldiği için her bir aya karşılık gelen dönemler.
months = {
    '3': ['Ocak', 'Şubat', 'Mart', 'January', 'February', 'March'],
    '6': ['Nisan', 'Mayıs', 'Haziran', 'April', 'May', 'June'],
    '9': ['Temmuz', 'Ağustos', 'Eylül', 'July', 'August', 'September'],
    '12': ['Ekim', 'Kasım', 'Aralık', 'October', 'November', 'December']
}

def news(stock_data: dict):

        #çıkış verisi olan stock_recordu başlat.
        stock_record = {}
        stock_record['stock_code'] = stock_data['stock_code']
        stock_record['periods'] = stock_data['periods']

        #Şirketin bizdeki dönemlerine göre haberleri yakalamak için periodları olası ay, yıl çiftlerine çevir.
        possibilities = []
        for index, period in enumerate(stock_data['periods']):
            month = str(period).split('/')[1]
            year = str(period).split('/')[0]
            for i in months[month]:
                possibilities.append({'month': i, 'year': year})
        
        # print(possibilities)

        #Toplam sayfa sayısını almak için ilk sayfayı çek.
        main_driver = get_driver()
        main_driver.get(f'https://www.getmidas.com/search/{stock_data['stock_code']}')

        #haber detayına gidebilmek için ikinci bir driver oluştur.
        detail_driver = get_driver()
        detail_wait = WebDriverWait(detail_driver, 10)

        page_count = 1
        try:
            page_count = main_driver.find_element(By.XPATH, '//div[@class="pagination-block"]/child::*[position()=last()-1]').text
        except Exception as e: 
            print('hata')


        periods_are_full = [False, False, False]
        for page in range(1, int(page_count) + 1):
            print(page, 'page')

            if False not in periods_are_full:
                break

            #ilk sayfa daha önce çekildiği için ilk sayfayı tekrar çekmeye gerek yok. İlk sayfa hariç çek.
            if page != 1:
                # print(f'https://www.getmidas.com/search/{stock_data['stock_code']}/page/{page}')
                main_driver.get(f'https://www.getmidas.com/search/{stock_data['stock_code']}/page/{page}')


            #Eğer bütün sayfalar çekilmişse veya gidilen sayfada kayıt yoksa ekrandaki 404 hatasını yakala ve döngüden çık.
            if len(main_driver.find_elements(By.CLASS_NAME, 'main-error-page')) > 0:
                print('Şirket Sayfa Sonu')
                break

            #sayfadaki bütün haber nesnelerini al.
            news_section = main_driver.find_element(By.CLASS_NAME, 'daily-newsletters-block')
            news = news_section.find_elements(By.CLASS_NAME, 'fadeInUp-scroll')
            
            for new in news:
                #haberin başlığı ve tarihini al.
                title = new.find_element(By.TAG_NAME, 'h4').get_attribute('textContent').lstrip().rstrip()
                date = new.find_element(By.TAG_NAME, 'span').get_attribute('textContent').rstrip().split('•')[0]
                print(f'AA{title}AA')
                print(f'AA{date}AA')

                #haber eğer aranan dönemde ise işleme devam edebilmek için değeri True yap.
                is_exists_in_possibilities = False
                period = ''
                for possibility in possibilities:
                    if date.find(possibility['month']) != -1 and date.find(possibility['year']) != -1:
                        print(date, possibility['month'], possibility['year'])
                        is_exists_in_possibilities = True
                        for key, value in months.items():
                            for month in value:
                                if possibility['month'] == month:
                                    period = f'{possibility['year']}/{key}'

                #stock_record çıkış dictinde default olarak periodları oluştur. boş olsalar bile çıkış verisinde olacaklar.
                if 'first_period' not in stock_record:
                    stock_record['first_period'] = []
                if 'second_period' not in stock_record:
                    stock_record['second_period'] = []
                if 'third_period' not in stock_record:
                    stock_record['third_period'] = []

                #Periodların haber kapasitesi dolduysa daha fazla haber alma.
                if len(list(stock_record['first_period'])) >= 10 and period == stock_data['periods'][0]:
                    periods_are_full[0] = True
                    continue
                if len(list(stock_record['second_period'])) >= 10 and period == stock_data['periods'][1]:
                    periods_are_full[1] = True
                    continue
                if len(list(stock_record['third_period'])) >= 10 and period == stock_data['periods'][2]:
                    periods_are_full[2] = True
                    continue

                #haber aranan dönemde ise işleme devam et.
                if is_exists_in_possibilities is True:

                    try:
                        new_detail_link = new.find_element(By.TAG_NAME, 'a')
                        # print(new_detail_link.get_attribute('href'))
                        detail_driver.get(str(new_detail_link.get_attribute('href')))

                        #bütün haber detaylarında ortak olan kapsayıcı article tagını al.
                        detail_article = detail_wait.until(EC.presence_of_element_located((By.TAG_NAME, 'article')))
                        # print(detail_article.get_attribute('textContent'))
                        FileManager('news.json').add_to_json({index: detail_article.get_attribute('textContent')})

                    except Exception as err:
                        print(err)
                        continue

                    #içeriği alınan haber hangi perioda denk geliyorsa ona göre çıkış verisine ekle.
                    if period == stock_data['periods'][0] and detail_article.text != '':
                        stock_record['first_period'].append(detail_article.text)
                    if period == stock_data['periods'][1] and detail_article.text != '':
                        stock_record['second_period'].append(detail_article.text)
                    if period == stock_data['periods'][2] and detail_article.text != '':
                        stock_record['third_period'].append(detail_article.text)  

        # Tarayıcıyı kapatın
        detail_driver.quit()
        main_driver.quit()
        return stock_record
