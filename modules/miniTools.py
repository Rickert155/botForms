from SinCity.colors import RED, RESET, GREEN, BLUE
from modules.config import base_dir, done_file_path, done_dir
import os, csv, sys

def InitBot():
    if not os.path.exists(done_dir):
        os.makedirs(done_dir)
    if not os.path.exists(done_file_path):
        with open(done_file_path, 'a') as file:
            file.close()

def ListBase():
    list_base = []
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        print(
                f'{RED}Директория {base_dir} создана!\n{RESET}'
                f'{RED}Необходимо добавить в нее базы{RESET}'
                )
        sys.exit()
    
    
    for base in os.listdir(base_dir):
        if '.csv' in base:
            list_base.append(f'{base_dir}/{base}')
    
    if len(list_base) == 0:
        print(f'{RED}Необходимо добавить базы в {base_dir}!{RESET}')
    return list_base

def CheckDoneDomains():
    list_domain = set()
    with open(done_file_path, 'r') as file:
        for line in file.readlines():
            domain = line.strip()
            if domain not in list_domain:
                list_domain.add(domain)

    return list_domain

def RecordingDoneDomain(domain:str):
    with open(done_file_path, 'a') as file:
        file.write(f'{domain}\n')

            
