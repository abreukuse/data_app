import pathlib

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent
DICTIONARY_MASTER = PACKAGE_ROOT / 'dictionary_master.json'
CITIES_LIST = PACKAGE_ROOT / 'cities_RS.txt'

PATH_UNZIPPED_FILES = PACKAGE_ROOT / 'unziped_files'
DOWNLOAD_PATH = PACKAGE_ROOT / 'download'
PATH_PREPROCESSED_DATA = PACKAGE_ROOT / 'preprocessed_data' 