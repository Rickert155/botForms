from SinCity.colors import RED, RESET, GREEN
from modules.config import analytics_dir
import os, sys, csv

def initAnalytics():
    if not os.path.exists(analytics_dir):
        os.makedirs(analytics_dir)
        print(
                f'{RED}Директория {analytics_dir} создана{RESET}\n'
                f'{RED}В нее необходимо добавить документы для обработки!{RESET}'
                )
        sys.exit()

def ListDocs():
    list_docs = []
    

if __name__ == '__main__':
    initAnalytics()
    list_docs = ListDocs()
    if len(list_docs) != 0:
        pass
    if len(list_docs) == 0:
        print(
                f'{RED}В директории {analytics_dir} '
                f'не обнаружено документов для обработки{RESET}'
                )
        sys.exit()

