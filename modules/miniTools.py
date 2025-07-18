from SinCity.colors import RED, RESET, GREEN, BLUE
from modules.config import base_dir
import os, csv, sys

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
            list_base.append(f'{base_dir}{base}')
    
    if len(list_base) == 0:
        print(f'{RED}Необходимо добавить базы в {base_dir}!{RESET}')
    return list_base
            
