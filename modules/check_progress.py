from modules.config import result_dir, base_name, done_file_path
import os, csv, time

def ListDocs():
    list_docs = []
    for doc in os.listdir(result_dir):
        if '.csv' in doc:list_docs.append(f'{result_dir}/{doc}')

    return list_docs

def ReadDoneDomain():
    list_domains = set()
    with open(done_file_path, 'r') as file:
        for line in file.readlines():
            domain = line.strip()
            list_domains.add(domain)

    print(f'Done domains: {len(list_domains)}\n')

sended_today = set()

count_domain = 0
sended_success = 0
not_connected = 0

def ReadDoc(doc:str):
    global count_domain, sended_success, not_connected, sended_today
    
    current_date = time.strftime("%d/%m/%Y")

    list_domains = set()
    with open(doc, 'r') as file:
        for row in csv.DictReader(file):
            domain = row['Domain']
            try:
                date = row['Time']
                if current_date in date:sended_today.add(domain)
            except:pass
            list_domains.add(domain)
    
    type_result = doc.split('/')[1]
    if '_' in type_result:type_result = type_result.replace('_', ' ')
    if '.csv' in type_result:type_result = type_result.replace('.csv', '')
    if base_name in type_result:type_result = type_result.replace(f'{base_name} ', '')
    if 'connected' in type_result:
        not_connected = len(list_domains)
    if len(type_result) <= 1:
        type_result = "success send"
        sended_success+=len(list_domains)
    type_result = type_result.strip()
    if 'not defined' in type_result:type_result = 'Не найдено форм'
    if 'unknown' in type_result:type_result = 'Форма с неизвестным полем'
    if 'success' in type_result:type_result = 'Успешная отправка'
    if 'redirect' in type_result:type_result = 'Редирект домена'
    if 'not connected' in type_result:type_result = 'Долгая загрузка страниц'
    print(f'{type_result} - {len(list_domains)}')
    count_domain+=len(list_domains)

if __name__ == '__main__':
    list_doc = ListDocs()
    ReadDoneDomain()
    for doc in list_doc:
        ReadDoc(doc=doc)
    current_sending = count_domain-not_connected
    exception_not_connectad = count_domain - not_connected
    percent_success = sended_success / (exception_not_connectad / 100) 
    print(
            f'\nУспешная обработка:\t{current_sending}\n'
            f'Процент отправленных:\t{round(percent_success, 2)} %\n'
            f'Проверено сегодня:\t{len(sended_today)}'
            )
