import pandas as pd
from pathlib import Path
from functools import lru_cache
from data.kontinente_laender_liste import country_to_continent_map as c2c_map


# dataframe laden und spaten benennen
@lru_cache(maxsize=5)
def load_data_annual(path: str) -> pd.DataFrame:

    df = pd.read_csv(path)
    df = df.rename(columns={"Entity": "country",
                            "Year": "year",
                            df.columns[-1]: "value"
                            })
    return df

# liste für die country dropdown 
# ( hier könnte man noch nach weiter filtern für 2 dropdowns z.b. continent und country)
def get_countries(path):

    df = load_data_annual(path)
    return sorted(df["country"].unique())

# list für die preselection dropdown
def get_preselection(path):

    country_list = get_countries(path)

    # Mapping anwenden
    categories = set()
    for country in country_list:
        if country in c2c_map:
            categories.add(c2c_map[country])

    return sorted(categories)

def get_countries_by_group(country_list, group_list):

    filtered = []
    for k in group_list:
        filtered = filtered + [country for country in country_list if c2c_map.get(country) == k]

    return sorted(filtered)

# year_range für den year slider
def get_year_range(path):

    df = load_data_annual(path)
    return int(df["year"].min()), int(df["year"].max())