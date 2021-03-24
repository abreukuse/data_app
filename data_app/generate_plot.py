"""
Creates the chart from plotly in the application.
"""

import pandas as pd
import plotly.express as px

def get_values(result_query):
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