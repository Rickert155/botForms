from selenium.webdriver.common.by import By

from SinCity.Browser.driver_chrome import driver_chrome
from SinCity.Browser.scrolling import Scrolling
from SinCity.colors import RED, RESET, BLUE, GREEN, YELLOW
from modules.miniTools import (
        divide_line,
        RecordingNotSended,
        RecordingSuccessSend
        )
from modules.content import GenerateContent
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

        Scrolling(driver=driver)

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
            submitForm(driver=driver, company=company)
            if submitForm == True:
                RecordingSuccessSend(domain=domain, company=company)
                return True
            
        if forms == False:
            list_pages = OtherPages(driver=driver, domain=domain)
            if len(list_pages) > 0:
                number_page=0
                check_forms = False
                for page in list_pages:
                    number_page+=1
                    print(f'{BLUE}[{number_page}] {page}{RESET}')
                    driver.get(page)
                    time.sleep(2)
                    Scrolling(driver=driver)
                    forms = SearchForms(driver=driver)
                    if forms != False:
                        check_forms = True
                        print(f'На странице контактов обнаружена форма')
                        submitForm(driver=driver, company=company)
                        if submitForm == True:
                            RecordingSuccessSend(domain=domain, company=company)
                            return True
                        if submitForm != True:
                            RecordingNotSended(
                                    domain=domain, 
                                    company=company,
                                    reason="unknown_field"
                                    )
                            return False
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
        count_input = 0
        for field_input in form.find_elements(By.TAG_NAME, 'input'):
            if field_input.is_displayed():
                count_input+=1

        if count_input >= 3:
            count_textarea=0
            for textarea in form.find_elements(By.TAG_NAME, 'textarea'):
                count_textarea+=1
            if count_textarea > 0:
                count_form+=1
    
        if count_form > 0:
            print(f'Форма {count_form}')
    
    
    if count_form == 0:
        return False

    return count_form

def submitForm(driver:str, company:str):
    number_form = 0
    for form in driver.find_elements(By.TAG_NAME, 'form'):
        number_form+=1
        count_input = 0
        count_textarea = 0
        for field_input in form.find_elements(By.TAG_NAME, 'input'):
            if field_input.is_displayed():
                count_input+=1

            if count_input >= 2:
                for textarea in form.find_elements(By.TAG_NAME, 'textarea'):
                    count_textarea+=1
        
        if count_textarea > 0:
            
            textarea = form.find_element(By.TAG_NAME, 'textarea')
            name_textarea = textarea.get_attribute('name')
            if 'g-recaptcha-response' in name_textarea:
                continue
            
            print(f'{YELLOW}Форма {number_form}{RESET}')
            content = GenerateContent(full_attrs="textarea", company=company)
            textarea.send_keys(content)
            time.sleep(2) 
            
            try:
                for field_input in form.find_elements(By.TAG_NAME, 'input'):
                    if field_input.is_displayed():

                        name = field_input.get_attribute('name')
                        placeholder = field_input.get_attribute('placeholder')
                        type_field = field_input.get_attribute('type')

                        full_attrs = f"{name} {placeholder} {type_field}"
                    
                        if type_field == 'email':
                            full_attrs = 'email'
                        if 'checkbox' in type_field:
                            try:
                                field_input.click()
                                print('Отметил чекбокс')
                                continue
                            except Exception as err:
                                print(f'error: {err}')
                        
                        if type_field == 'submit':
                            continue

                        content = GenerateContent(full_attrs=full_attrs, company=company)
                        print(
                                f'Placeholder: {placeholder}\n'
                                f'Type: {type_field}\n'
                                f'Name: {name}\n'
                                )
                        if 'checkbox' not in type_field and 'submit' not in type_field:
                            field_input.send_keys(content)
                            time.sleep(2)

                submit = form.find_element(By.CSS_SELECTOR, '[type="submit"]')
                submit.click()
                print(f'{GREEN}Форма успешно отправлена!{RESET}')
                time.sleep(2)
                return True
            except Exception:
                print(f'{RED}Error: {err}{RESET}')
                return False

    return False


if __name__ == '__main__':
    params = sys.argv
    if len(params) > 1:
        domain = params[1]
        ProcessingDomain(domain=domain, company='Testing Company')
    if len(params) == 1:
        print(f'Передай параметром домен')
        sys.exit()
