from pathlib import Path
import os

PARENT_DIR = Path(__file__). parent.resolve().parent
DATA_DIR = PARENT_DIR / 'data'
RAW_DATA_DIR = PARENT_DIR / 'data' / 'raw'
TRANSFORMED_DATA_DIR = PARENT_DIR / 'data' / 'transformed'

if not Path(RAW_DATA_DIR).exists():
    os.mkdir(RAW_DATA_DIR)

if not Path(TRANSFORMED_DATA_DIR).exists():
    os.mkdir(TRANSFORMED_DATA_DIR)