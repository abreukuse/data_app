# This code automatically downloads the open data from the 
# Foundation for Economics and Statistics (Fundação de Economia e Estatística) web site: 
# https://dados.fee.tche.br/index.php
# using the Selenium tool.

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from config import DOWNLOAD_PATH

def run_download():
    path_download = DOWNLOAD_PATH
    print(f'Download directory: {path_download}')
    if not os.path.isdir(path_download):
        os.mkdir(path_download)
    else:
        pass

    chrome_options = webdriver.ChromeOptions()
    preferences = {
                    "profile.default_content_settings.popups": 0,
                    "download.default_directory": path_download,
                    "directory_upgrade": True
                  }
    chrome_options.add_experimental_option('prefs', preferences)

    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options) # instalar chrome driver
    time.sleep(5)
    driver.implicitly_wait(30) # expects to load things from the page
    driver.get('https://dados.fee.tche.br') # opens the browser
    driver.maximize_window() # maximizar
    driver.find_element_by_id('unidadegeo').click() # opens the dropdown list
    driver.find_element_by_xpath('//*[@id="unidadegeo"]/option[3]').click() # select municipalities in dropdown options

    # opens all exposed folders
    uma_camada = driver.find_elements_by_class_name('dynatree-title') # find all folders exposed on the site

    nomes_uma_camada = [] # list in which it will be saved the folder names

    # loop to get folder names and click on them
    for pasta in uma_camada:
        titulo = pasta.get_attribute('title')
        nomes_uma_camada.append(titulo)
        pasta.click()
 
   
    # list in which the previous layers will be stored.
    # Something needed for the procedure
    nomes_camadas_anteriores = [nomes_uma_camada] 

    # loop that will open all hidden subfolders
    for i in range(4):
        camadas = driver.find_elements_by_class_name('dynatree-title')
        
        nomes_camadas = []
        for each in camadas:
            titulo = each.get_attribute('title')
            nomes_camadas.append(titulo)

        dicionario = list(zip(nomes_camadas, camadas)) # dictionary of everything
        copia = dicionario[:]
        
        anterior = nomes_camadas_anteriores[i]
        for i, cada in zip(range(len(dicionario)), nomes_camadas):
            if cada in anterior:
                copia.remove((dicionario[i][0], dicionario[i][1])) 

        for i in range(len(copia)):
            if 'Abrir Pasta' in copia[i][0]:
                copia[i][1].click()
                
        nomes_camadas_anteriores.append(nomes_camadas)
            
    # this list has some folder names that didn’t open in the previous step because some of them have the same name
    falta_abrir = ['Abrir Pasta: Palmito', 
                   'Abrir Pasta: Número de Estabelecimentos',
                   'Abrir Pasta: Madeira em Tora',
                   'Abrir Pasta: Faixa Etária',
                   'Abrir Pasta: Ensino Fundamental',
                   'Abrir Pasta: Ensino Médio',
                   'Abrir Pasta: Valor Adicionado Bruto a Preços Básicos']

    # folders that are still closed
    remanescentes = [(dicionario[i][0], dicionario[i][1]) for i in range(len(dicionario)) if dicionario[i][0] in falta_abrir]
    clicar = [each[1] for i, each in (enumerate(remanescentes)) if i not in [1,2,4,9,12,14,16,17,23]] # do not include folders that are already open

    # open the missing folders
    for cada in clicar:
        cada.click()
        
    # DOWNLOAD json files
    todos = driver.find_elements_by_class_name('dynatree-title') # list of everything that is open
    nomes = []
    for cada in todos:
        nomes.append(cada.get_attribute('title')) # generate list with the names of everything

    total = list(zip(nomes, todos)) # concatenates names with values

    # loop to download the files
    for cada in total:
        if 'Selecionar Variável' in cada[0]:
            try:
                cada[1].click()
                driver.find_element_by_xpath('//*[@id="div_anos"]/fieldset/button[1]').click() # select every year
                driver.find_element_by_id('link_json').click() # download the jsons
            except:
                print('erro em -->', titulo, cada[0])

    driver.close()

if __name__ == "__main__":
    run_download()