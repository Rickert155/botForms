from selenium.webdriver.common.by import By

from SinCity.Browser.driver_chrome import driver_chrome
from SinCity.colors import RED, RESET, BLUE, GREEN
from modules.miniTools import (
        divide_line,
        RecordingNotSended,
        RecordingSuccessSend
        )
from modules.config import contact_pages
import sys, time

"""Ищем страницы контактов(или где может быть контактная форма)"""
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
        
"""Вводная функция обработки домена"""
def ProcessingDomain(domain:str, company:str):
    driver = None
    try:
        driver = driver_chrome()
        driver.get(f'https://{domain}')
        time.sleep(2)
        current_url = driver.current_url

        if domain not in current_url:
            current_domain = current_url.split('://')[1]
            print(f'{RED}Редирект {domain} -> {current_domain}{RESET}')
            RecordingNotSended(domain=domain, company=company, reason="redirect")
            if driver != None:
                driver.quit()
            return False

        forms = SearchForms(driver=driver)

        if forms != False:
            print('Тут будет функция для заполнения формы')
        if forms == False:
            list_pages = OtherPages(driver=driver, domain=domain)
            if len(list_pages) > 0:
                number_page=0
                check_forms = False
                for page in list_pages:
                    number_page+=1
                    print(f'{BLUE}[{number_page}] {page}{RESET}')
                    driver.get(page)
                    forms = SearchForms(driver=driver)
                    if forms != False:
                        check_forms = True
                        print(f'На странице контактов обнаружена форма')
                        return
                if check_forms == False:
                    print(f'{RED}На страницах контактов не обнаружены формы!{RESET}')
                    RecordingNotSended(domain=domain, company=company, reason="not defined")
                    return
            if len(list_pages) == 0:
                print(f'{RED}Страницы контактов не обнаружены{RESET}')
                RecordingNotSended(domain=domain, company=company, reason="not defined")
                return


    except KeyboardInterrupt:
        print(f'{RED}\nExit...{RESET}')
        sys.exit()

    finally:
        if driver != None:
            driver.quit()
        print(divide_line())


"""Поиск формы на странице"""
def SearchForms(driver:str):
    count_form = 0
    for form in driver.find_elements(By.TAG_NAME, 'form'):
        count_form+=1
        print(f'Форма {count_form}')
    
    
    if count_form == 0:
        return False

    return count_form
    


if __name__ == '__main__':
    params = sys.argv
    if len(params) > 1:
        domain = params[1]
        ProcessingDomain(domain=domain, company='Testing Company')
    if len(params) == 1:
        print(f'Передай параметром домен')
        sys.exit()
