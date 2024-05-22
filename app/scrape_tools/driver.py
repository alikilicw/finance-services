from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def get_driver() -> webdriver.Firefox:
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    return driver