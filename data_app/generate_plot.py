"""
Creates the chart from plotly in the application.
"""

import pandas as pd
import plotly.express as px

def get_values(result_query):
    """
    Get the necessary values in the returned query from mongodb
    --------------------------
    parameter:
    result_query - A dictionary resulting from the list of documents extracted from mongodb

    return: 
    dictionary with claen values
    """
    dictionary = {}
    dictionary['city'] = result_query['nome']
    for each in result_query['valores']:
        for variable in ['ano','unidade','valor']:
            include = None if each[variable] == '-' else each[variable]
            dictionary.setdefault(variable, []).append(include)

    dictionary['valor'] = [float(item.replace('.', '_').replace(',', '.')) 
						  if item != None else None 
						  for item in dictionary['valor']]
                          
    dictionary['ano'] = [int(item) for item in dictionary['ano']]
    return dictionary


def build_dataframe(documents):
    """
    Build a pandas dataframe from the result of the above function
    ----------------------------------
    parameter.
    documents: List with all the documents gathered from the database

    return:
    dataframe
    """
    dataframes = []
    for document in documents:
        dictionary = get_values(document)
        df = pd.DataFrame.from_dict(dictionary)
        df = df.dropna(how='any', subset=['ano','valor']).reset_index(drop=True)
        if '$' in df['unidade'][0]:
            df = df.query('ano >= 1994').reset_index(drop=True)
        dataframes.append(df)
    return pd.concat(dataframes).reset_index(drop=True)


def visualize(dataframe, title='Title'):
    """
    Generate the visualization in the app
    -------------------------------------
    parameters:
    dataframe - A pandas dataframe built from the abive function
    title - plot´s title

    return:
    plotly figure
    """
    unity = dataframe['unidade'][0] if dataframe['unidade'][0] != None else 'Quantidade'
    fig = px.line(dataframe, 
                  x='ano',
                  y='valor',
                  title=title,
                  color='city',
                  width=900,
                  height=500,
                  labels={'valor': unity,'ano': 'Ano'})\
    .for_each_trace(lambda x: x.update(name=x.name.replace('city=','')))
    return fig