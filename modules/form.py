from selenium.webdriver.common.by import By

from SinCity.Browser.driver_chrome import driver_chrome
from SinCity.colors import RED, RESET, BLUE, GREEN
from modules.config import contact_pages
import sys, time

def OtherPages(driver:str, domain:str):
    list_link = set()
    for link in driver.find_elements(By.TAG_NAME, 'a'):
        link = link.get_attribute('href')
        if link:
            if domain in link and '#' not in link and 'mailto:' not in link:
                for page in contact_pages:
                    if page in link:
                        if link[-1] == '/':link = link[:-1]
                        list_link.add(link)

    return list_link
        

def ProcessingDomain(domain:str, company:str):
    driver = driver_chrome()
    driver.get(f'https://{domain}')
    time.sleep(2)
    list_pages = OtherPages(driver=driver, domain=domain)
    if len(list_pages) > 0:
        number_page=0
        for page in list_pages:
            number_page+=1
            print(f'{BLUE}[{number_page}] {page}{RESET}')

    driver.quit()
    print('')


if __name__ == '__main__':
    params = sys.argv
    if len(params) > 1:
        domain = params[1]
        ProcessingDomain(domain=domain, company='Testing Company')
    if len(params) == 1:
        print(f'Передай параметром домен')
        sys.exit()
