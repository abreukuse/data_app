import streamlit as st
import numpy as np
import json
from functools import reduce
import operator
from ast import literal_eval
from mongodb_query import find_document
from generate_plot import get_values, build_dataframe, visualize

st.set_page_config(layout="wide")

@st.cache(show_spinner=False)
def load_dict():
    """Load the dictionary with all the keys and the list with all the cities."""
    with open('dictionary_master.json', 'r', encoding='latin1') as json_file:
        dictionary_master = json.load(json_file)

    with open('cities_RS.txt', 'r', encoding='latin1') as txt_file:
        cities = [literal_eval(line) for line in txt_file][0]

    return dictionary_master, cities

dictionary_master, cities = load_dict()

st.title('Data App')
city = st.sidebar.selectbox('Selecione a cidade', [''] + cities, index=0)

def getFromDict(dataDict, mapList):
    """
    Access all the next keys in a nested dictionary from a list of previous keys.
    ------------------------------------------------------
    dataDict: Dictionary containind all the keys necessary.
    mapList: List which the elements in order provide a specific path inside the dictionary.
    """
    result = reduce(operator.getitem, mapList, dataDict)
    if isinstance(result, dict):
        return list(result.keys())
        

options = list(dictionary_master.keys())

keys = []
def dropdown(last_dropdown, options, id_):
    """
    Generate the dropdown widgets in the web app from which the user can select their desired data visializaation.
    This function is used in a recursive manner: The nex dropdown is created from the last one and so forth.
    -------------------------------------------------
    last_dropdown: The option chosed by the user in the last dropdown
    options: The options available in the current dropdown
    id_: This is the key arguemnt required in the selectbox from streamlit.
    """
    if last_dropdown != '':
        options = [''] + options
        next_dropdown = st.sidebar.selectbox('', options=options, index=0, key=id_)
        id_ += 1

        if next_dropdown != '':
            keys.append(next_dropdown) 

        options = getFromDict(dictionary_master, keys)
        if options != None:
            # st.write(keys)
            return dropdown(last_dropdown=next_dropdown, options=options, id_=id_)
        if options == None:
            query = '.'.join(keys)
            st.write(' - '.join(keys))
            return query


if __name__ == '__main__':
    query = dropdown(last_dropdown=city, options=options, id_=1)
    if isinstance(query, str):
        try:
            result_query = find_document(query=query, city=city)
            print(result_query)
            values = get_values(result_query=result_query)
            dataframe = build_dataframe(dictionary=values)
            st.plotly_chart(visualize(dataframe, city))
        except:
            st.write('A busca não obteve resultado.')