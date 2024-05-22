from .driver import get_driver
from selenium.webdriver.common.by import By
from core.utils.text_convert import text_convert

pages = ['bilanco', 'gelir-tablosu']

kalemler = [
    "toplam_varliklar",
    "toplam_ozkaynaklar",
    "brut_kar_(zarar)",
    "donem_kari_(zarari)"
]

def get_financial_tables(stock_code: str) -> dict:

    financial_tables = {}

    driver = get_driver()
    for page in pages:

        url = f'https://fintables.com/sirketler/{stock_code}/finansal-tablolar/{page}'
        driver.get(url)

        main_title = driver.find_element(By.XPATH, '//div[@class="px-4 pb-4 pt-4 text-sm text-foreground-01"]')
        x = main_title.find_element(By.XPATH, f'./table[1]/thead/tr')
        title_list = x.find_elements(By.TAG_NAME, 'th')

        for i in range(4, 0, -1):
            print(title_list[i].text)
            row_sections = main_title.find_elements(By.XPATH, f'./table[2]/tbody')

            for row_section in row_sections:

                rows = row_section.find_elements(By.TAG_NAME, 'tr')

                for index, row in enumerate(rows):

                    #her bir kümenin içindeki satırların sonunda boş birer satır daha var. onları alma.
                    if index + 1 == len(rows):
                        continue

                    values = row.find_elements(By.TAG_NAME, 'td')
                    value_name = text_convert(values[0].text)
                    value = values[i].text

                    #mali kalem bizim istediklerimizden biri mi?
                    if value_name in kalemler:

                        # current period şirket kaydının içinde var mı? yoksa boş bir şekilde oluştur.
                        if title_list[i].text not in financial_tables:
                            financial_tables[title_list[i].text] = {}
                        if value_name not in financial_tables[title_list[i].text]:
                            financial_tables[title_list[i].text][str(value_name)] = value
        
    driver.quit()
    return {
        'financial_tables': financial_tables,
        'stock_code': stock_code
    }
    