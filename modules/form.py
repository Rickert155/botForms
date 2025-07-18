from selenium.webdriver.common.by import By

from SinCity.Browser.driver_chrome import driver_chrome
import sys

def ProcessingDomain(domain:str, company:str):
    driver = driver_chrome()
    driver.get(f'https://{domain}')
    print(domain)
    driver.quit()


if __name__ == '__main__':
    params = sys.argv
    if len(params) > 1:
        domain = params[1]
        ProcessingDomain(domain=domain, company='Testing Company')
    if len(params) == 1:
        print(f'Передай параметром домен')
        sys.exit()
