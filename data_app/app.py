"""
Build the web app.
"""

import streamlit as st
import json
from functools import reduce
import operator
from ast import literal_eval
from mongodb_query import find_document
from generate_plot import get_values, build_dataframe, visualize
from config import FILES

st.set_page_config(layout="wide")

@st.cache(show_spinner=False)
def show_introduction():
    introduction = """
    ## Visualização de Séries Temporais de Fatores Socioeconômicos do Estado do Rio Grande do Sul

    Com essa aplicação é possível  visualizar dados de séries temporais de diversos fatores socioeconômicos do estado do Rio Grande do Sul. Os dados foram coletados do site da [Fundação de Economia e Estatística](https://dados.fee.tche.br/index.php).<br>
    Para gerar uma visualização, selecione à esquerda até três cidades que você gostaria de saber alguma informação e novas opções de busca irão surgindo.<br> 
    Alguns exemplos de dados que podem ser acessados são:  Agricultura, Comércio, Comunicações, Demografia, Educação, Emprego, Saúde, Segurança, Transportes entre outros.
    Informações sobre o significado de cada variável socioeconômica pode ser vista nesse [link](http://deedados.planejamento.rs.gov.br/feedados/#!home/descricaovariaveis).

    [Tobias de Abreu Kuse](https://www.linkedin.com/in/tobias-de-abreu-kuse/)<br>
    [github](https://github.com/abreukuse/data_app) 
    """
    return introduction

@st.cache(show_spinner=False)
def load_dict():
    """Load the dictionary with all the keys and the list with all the cities."""
    path_dictionary = FILES / 'dictionary_master.json'
    with open(path_dictionary, 'r', encoding='latin1') as json_file:
        dictionary_master = json.load(json_file)

    path_list = FILES / 'cities_RS.txt'
    with open(path_list, 'r', encoding='latin1') as txt_file:
        cities = [literal_eval(line) for line in txt_file][0]

    return dictionary_master, cities

st.markdown(show_introduction(), unsafe_allow_html=True)
dictionary_master, cities = load_dict()

# All cities listed in a dropdown
municipalities = st.sidebar.multiselect('Selecione até três cidades', cities)

def getFromDict(dataDict, mapList):
    """
    Access all the next keys in a nested dictionary from a list of previous keys.
    ------------------------------------------------------
    dataDict: Dictionary containind all the keys necessary.
    mapList: List in which the items in order, provide a specific path inside the dictionary.
    """
    result = reduce(operator.getitem, mapList, dataDict)
    if isinstance(result, dict):
        return list(result.keys())
        
# Options available in the first dropdown
options = list(dictionary_master.keys())

keys = []
def dropdown(last_dropdown, options, id_):
    """
    Generate the dropdown widgets in the web app from which the user can select their desired data visializaation.
    This function is used in a recursive manner: The next dropdown is created from the last one and so forth.
    -------------------------------------------------
    last_dropdown: The option chosen by the user in the last dropdown
    options: The options available in the current dropdown
    id_: This is the key argument required in the selectbox from streamlit.
    """
    if len(last_dropdown) != 0:
        options = [''] + options
        next_dropdown = st.sidebar.selectbox('', options=options, index=0, key=id_)
        id_ += 1

        if next_dropdown != '':
            keys.append(next_dropdown) 

        options = getFromDict(dictionary_master, keys)
        if options != None:
            return dropdown(last_dropdown=next_dropdown, options=options, id_=id_)
        if options == None:
            query = '.'.join(keys)
            st.write('Gerando o Gráfico:')
            return query


if __name__ == '__main__':
    query = dropdown(last_dropdown=municipalities, options=options, id_=1)
    if isinstance(query, str):
        try:

            result_query = find_document(query=query, cities=municipalities)
            dataframe = build_dataframe(documents=result_query)
            st.plotly_chart(visualize(dataframe=dataframe, title=query))

        except Exception as e:
            print(e)
            st.write('A busca não obteve resultado.')