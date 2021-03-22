import pathlib

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent
FILES = PACKAGE_ROOT / 'files'
PATH_UNZIPPED_FILES = PACKAGE_ROOT / 'unziped_files'
DOWNLOAD_PATH = PACKAGE_ROOT / 'download'
PATH_PREPROCESSED_DATA = PACKAGE_ROOT / 'preprocessed_data' 