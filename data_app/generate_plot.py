"""
Creates the chart from plotly in the application.
"""

import pandas as pd
import plotly.express as px

def get_values(result_query):
  	"""Get the values in the returned query from mongodb"""
	dictionary = {}
	for each in result_query['valores']:
		for variable in ['ano','unidade','valor']:
			include = None if each[variable] == '-' else each[variable]
			dictionary.setdefault(variable, []).append(include)

	dictionary['valor'] = [int(item.replace('.', '')) if item != None else None for item in dictionary['valor']]
	dictionary['ano'] = [int(item) for item in dictionary['ano']]
	return dictionary

def build_dataframe(dictionary):
	"""Build a pandas dataframe from the result of the function above"""
	df = pd.DataFrame.from_dict(dictionary)
	df = df.dropna(how='any', subset=['ano','valor']).reset_index(drop=True)
	if (df['unidade'][0] != None) and ('$' in df['unidade'][0]):
		df = df.query('ano >= 1994').reset_index(drop=True)
	return df

def visualize(dataframe, title='Title'):
	"""Generate the visualization in the app from the dataframe created in the above function"""
	unity = dataframe['unidade'][0] if dataframe['unidade'][0] != None else 'Quantidade'
	fig = px.line(dataframe, 
				  x='ano', 
				  y='valor',
				  title=title,
				  width=900,
				  height=500,
				  labels={'valor': unity,
						  'ano': 'Ano'})
	return fig