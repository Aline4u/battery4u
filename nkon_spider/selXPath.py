import re, itertools
from selenium import webdriver
from bs4 import BeautifulSoup as BS
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if siblings == [child] else
            '%s[%d]' % (child.name, 1 + siblings.index(child))
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

def main():
    # driver = webdriver.PhantomJS(executable_path='phantomjs.exe')
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) as driver:
        # driver.get(url)
        driver.get("  ")

    buttons = driver.find_elements(By.XPATH,'//button[@data-test-id="seemoretoggle"]');
    for btn in buttons:
        btn.click()

    html = driver.page_source
    soup = BS(html, 'html.parser')
    elem = soup.find(string=re.compile('Tiny House interior'))
    print(elem)
    xpath_soup(elem)
    print(xpath_soup(elem))

if __name__ == '__main__':
    main()

