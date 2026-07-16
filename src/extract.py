import pandas as pd

from src.config import RAW_DIR


def load_csv(filename):

    path = RAW_DIR / filename

    return pd.read_csv(path)