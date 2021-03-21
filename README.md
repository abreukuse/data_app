## Data visualization app
At the moment I live in south of Brazil in a state called Rio Grande do Sul. A state agency called Foundation of economy and statics ([Fundação de Economia e Estatística](https://dados.fee.tche.br/index.php) in portuguese) provides raw data about several socioeconomic variables. Some examples are: Agriculture, Commerce, Education, Health Care, Transportation and many others. An explanation about each variable can be seen [here](http://deedados.planejamento.rs.gov.br/feedados/#!home/descricaovariaveis) (in portuguese).

I`m building this simple web application where one can easily access time series visualization from any of the social and economic sectors available. For now, one time series can be visualize at a time, but I will keep adding features to support comparison between different variables.

### Steps

In order to reproduce the application yourself locally, there´s a number of steps that need to be made.<br>
As a first step you need to clone the repo and ensure that you have installed the required packages in the [`requirements.txt`](https://github.com/abreukuse/data_app/blob/master/requirements.txt) file.

#### Data gathering

The data were collected from [this](https://dados.fee.tche.br/index.php) web site with the help of [`selenium`](https://selenium-python.readthedocs.io/) library. In order to automatically download all the files, run the script called [`download_data.py`](https://github.com/abreukuse/data_app/blob/master/data_app/download_data.py) inside the data_app folder. The files will be stored in the `download` directory.

#### Data preprocessing

In this step you need to run the [`preprocessing_json.py`](https://github.com/abreukuse/data_app/blob/master/data_app/preprocessing_json.py) script. This scrip will unzip all the files and store them in the `unziped_files` folder. After that, it will preprocess each file in order to put them in the desired shape for importing them in a MongoDB database. These files can be encountered in the `preprocessed_data` directory.<br>
Also, you need to execute the file [`create_cities_RS_list.py`](https://github.com/abreukuse/data_app/blob/master/data_app/create_cities_RS_list.py). This script gets, from the wikipedia [page](https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Rio_Grande_do_Sul), the names of all the 497 cities that compose the Rio Grande do Sul state and store them as a list in the `cities_RS.txt` file.

#### Data storage

To store the data in MongoDB, the script [`data_storage_mongodb.py`](https://github.com/abreukuse/data_app/blob/master/data_app/data_storage_mongodb.py) need to be executed. The database `fee_database` and collection `collections` will be created.<br>
Another step that need to be made at this point is to run the script [`embedded_documents.py`](https://github.com/abreukuse/data_app/blob/master/data_app/embedded_documents.py). This script will create a file called `dictionary_master.json`. This file is a nested dictionary and contains all the paths to reach the data values.

#### Data visualization

The [`generate_plot.py`](https://github.com/abreukuse/data_app/blob/master/data_app/generate_plot.py) script is responsible for create the time series charts. This module is executed inside the [`app.py`](https://github.com/abreukuse/data_app/blob/master/data_app/app.py) file, so there´s no need to run it by itself.

#### App deployment

The web app user interface was made possible using the library [streamlit](https://streamlit.io/) and can be seen running the command: `streamlit run app.py`. The deployment in the platform [Heroku](https://www.heroku.com/) will be explained soon.

