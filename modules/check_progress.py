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

def ReadDoc(doc:str):
    list_domains = set()
    with open(doc, 'r') as file:
        for row in csv.DictReader(file):
            domain = row['Domain']
            list_domains.add(domain)
    
    type_result = doc.split('/')[1]
    if '_' in type_result:type_result = type_result.replace('_', ' ')
    if '.csv' in type_result:type_result = type_result.replace('.csv', '')
    if base_name in type_result:type_result = type_result.replace(f'{base_name} ', '')
    print(f'{type_result} - {len(list_domains)}')

if __name__ == '__main__':
    list_doc = ListDocs()
    ReadDoneDomain()
    for doc in list_doc:
        ReadDoc(doc=doc)
