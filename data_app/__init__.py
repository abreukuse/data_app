import pathlib

PACKAGE_ROOT = pathlib.Path(data_app.__file__).resolve().parent
VERSION_PATH = PACKAGE_ROOT / 'VERSION'
