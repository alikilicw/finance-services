from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

def get_stock_price(month, year, stock_code, driver: webdriver.Firefox) -> str:

    try:
        url = f'https://www.strateji.com.tr/tr/bist/hisseler-tarihsel/index.asp'
        driver.get(url)
        wait = WebDriverWait(driver, 3)

        stock_rows = ''
        for i in range(1, 30):
            try:

                day_select = driver.find_element(By.NAME, 'ilk_gun')
                month_select = driver.find_element(By.NAME, 'ilk_ay')
                year_select = driver.find_element(By.NAME, 'ilk_yil')

                select_day = Select(day_select)
                select_month = Select(month_select)
                select_year = Select(year_select)

                select_day.select_by_value(f'{i}')
                select_month.select_by_value(f'{month}')
                select_year.select_by_value(f'{year}')
                driver.find_element(By.NAME, 'gonder').click()

                stock_rows = wait.until(EC.presence_of_element_located((By.XPATH, f'//ul[@id="Abc"]')))
                break
            except:
                pass            

        stock_rows_ = stock_rows.find_elements(By.TAG_NAME, 'li')
        
        for stock_row in stock_rows_:
            if stock_code == stock_row.find_element(By.TAG_NAME, 'div').get_attribute('data-value'):
                value = stock_row.find_elements(By.TAG_NAME, 'p')[2].text
                return value
            

    except Exception as err:
            print(err)
            