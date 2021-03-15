# Este código baixa automaticamente os dados abertos da Fundação de Economia e Estatística
# usando a ferramenta Selenium.

# https://dados.fee.tche.br/index.php

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def run_download():
    path_download = os.getcwd() + '\\download\\'
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
    driver.implicitly_wait(30) # espera carregar as coisas da página
    driver.get('https://dados.fee.tche.br') # abre o navegador
    driver.maximize_window() # maximizar
    driver.find_element_by_id('unidadegeo').click() # abre a lista do drop down
    driver.find_element_by_xpath('//*[@id="unidadegeo"]/option[3]').click() # seleciona municípios nas opções do dropdown

    # abre todas as pastas expostas
    uma_camada = driver.find_elements_by_class_name('dynatree-title') # encontro todas as pastas expostas no site

    nomes_uma_camada = [] # lista em que vou guardar os nomes das pastas

    # loop para pegar os nomes das pastas e clicar nelas
    for pasta in uma_camada:
        titulo = pasta.get_attribute('title')
        nomes_uma_camada.append(titulo)
        pasta.click()
 
    # lista em que serão armazenadas as camadas anteriores.
    # Algo necessário para o procedimento
    nomes_camadas_anteriores = [nomes_uma_camada] 

    # loop que irá abrir todas as sub pastas escondidas
    for i in range(4):
        camadas = driver.find_elements_by_class_name('dynatree-title')
        
        nomes_camadas = []
        for each in camadas:
            titulo = each.get_attribute('title')
            nomes_camadas.append(titulo)

        dicionario = list(zip(nomes_camadas, camadas)) # dicionario de tudo
        copia = dicionario[:]
        
        anterior = nomes_camadas_anteriores[i]
        for i, cada in zip(range(len(dicionario)), nomes_camadas):
            if cada in anterior:
                copia.remove((dicionario[i][0], dicionario[i][1])) 

        for i in range(len(copia)):
            if 'Abrir Pasta' in copia[i][0]:
                copia[i][1].click()
                
        nomes_camadas_anteriores.append(nomes_camadas)
            
    # essa lista possui alguns nomes de  pastas que não abriram no passo anterior porque algumas delas possuem o mesmo nome 
    falta_abrir = ['Abrir Pasta: Palmito', 
                   'Abrir Pasta: Número de Estabelecimentos',
                   'Abrir Pasta: Madeira em Tora',
                   'Abrir Pasta: Faixa Etária',
                   'Abrir Pasta: Ensino Fundamental',
                   'Abrir Pasta: Ensino Médio',
                   'Abrir Pasta: Valor Adicionado Bruto a Preços Básicos']

    # pastas ainda fechadas
    remanescentes = [(dicionario[i][0], dicionario[i][1]) for i in range(len(dicionario)) if dicionario[i][0] in falta_abrir]
    clicar = [each[1] for i, each in (enumerate(remanescentes)) if i not in [1,2,4,9,12,14,16,17,23]] # não incluir as pastas que já estão abertas

    # abrir as pasta que faltam
    for cada in clicar:
        cada.click()
        
    # DOWNLOAD dos arquivos json
    todos = driver.find_elements_by_class_name('dynatree-title') # lista de tudo o que está aberto
    nomes = []
    for cada in todos:
        nomes.append(cada.get_attribute('title')) # gera lista com os nomes de tudo

    total = list(zip(nomes, todos)) # concatena os nomes com os valores

    # loop para baixar os arquivos
    for cada in total:
        if 'Selecionar Variável' in cada[0]:
            try:
                cada[1].click()
                driver.find_element_by_xpath('//*[@id="div_anos"]/fieldset/button[1]').click() # selecionar todos os anos
                driver.find_element_by_id('link_json').click() # baixar os jsons
            except:
                print('erro em -->', titulo, cada[0])

    driver.close()

if __name__ == "__main__":
    run_download()