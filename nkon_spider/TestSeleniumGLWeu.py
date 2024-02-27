import re, itertools
from selenium import webdriver
from bs4 import BeautifulSoup as BS
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By


def main():
    # driver = webdriver.PhantomJS(executable_path='phantomjs.exe')
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) as driver:
        # driver.get(url)
        driver.get("https://shop.gwl.eu/LiFePO4-Single-Cells/")

    # buttons = driver.find_elements(By.XPATH,'//button[@data-test-id="seemoretoggle"]');
    # for btn in buttons:
    #     btn.click()
    robotparser =
    html = driver.page_source
    with open('glw.htm', 'w') as f:
        f.write(html)
    soup = BS(html, 'html.parser')
    elem = soup.find(string=re.compile('ThunderSky'))
    print(elem)
    xpath_soup(elem)
    print(xpath_soup(elem))

if __name__ == '__main__':
    main()
