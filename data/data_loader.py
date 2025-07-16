import pandas as pd
from pathlib import Path
from functools import lru_cache


# dataframe laden und spaten benennen
@lru_cache(maxsize=5)
def load_data_annual(path: str) -> pd.DataFrame:

    df = pd.read_csv(path)
    df = df.rename(columns={"Entity": "country",
                            "Year": "year",
                            df.columns[-1]: "value"
                            })
    return df

# liste für die dropdown funktion
# ( hier könnte man noch nach weiter filtern für 2 dropdowns z.b. continent und country)
def get_countries(path):

    df = load_data_annual(path)
    return sorted(df["country"].unique())

# year_range für den year slider
def get_year_range(path):

    df = load_data_annual(path)
    return int(df["year"].min()), int(df["year"].max())