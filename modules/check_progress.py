from modules.config import result_dir, base_name, done_file_path
import os, csv

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

count_domain = 0
sended_success = 0

def ReadDoc(doc:str):
    global count_domain, sended_success

    list_domains = set()
    with open(doc, 'r') as file:
        for row in csv.DictReader(file):
            domain = row['Domain']
            list_domains.add(domain)
    
    type_result = doc.split('/')[1]
    if '_' in type_result:type_result = type_result.replace('_', ' ')
    if '.csv' in type_result:type_result = type_result.replace('.csv', '')
    if base_name in type_result:type_result = type_result.replace(f'{base_name} ', '')
    if len(type_result) <= 1:
        type_result = "success send"
        sended_success+=len(list_domains)
    type_result = type_result.strip()
    print(f'{type_result} - {len(list_domains)}')
    count_domain+=len(list_domains)

if __name__ == '__main__':
    list_doc = ListDocs()
    ReadDoneDomain()
    for doc in list_doc:
        ReadDoc(doc=doc)
    print(f'\ncurrent sending: {count_domain}')
    percent_success = sended_success / (count_domain / 100)
    print(f'\npercent sended: {round(percent_success, 2)} %')
