from .scraping import year_data_exists, all_data_exists
from .scraping import get_all_contests, get_year_data

import pandas as pd


def get_by_country(country, data=None):
    if data is None:
        data = get_all_contests()
    return data[data["Country"] == country].reset_index(drop=True)


def get_most_participations(top=5, data=None):
    if data is None:
        data = get_all_contests()
    return data["Name"].value_counts().head(top)


def get_best_contestants(top=5, country=None, data=None):
    if type(top) != int:
        country = top
        top = 5
    if data is None:
        data = get_all_contests()
    if country is not None:
        data = get_by_country(country)
    n_gold = data[data["Award"] == "Gold"]["Name"].value_counts()
    n_silver = data[data["Award"] == "Silver"]["Name"].value_counts()
    n_bronze = data[data["Award"] == "Bronze"]["Name"].value_counts()
    n_participations = data["Name"].value_counts()

    df = (
        pd.DataFrame(
            {
                "Gold": n_gold,
                "Silver": n_silver,
                "Bronze": n_bronze,
                "Participations": n_participations,
            }
        )
        .fillna(0)
        .astype(int)
    )

    df.sort_values(
        by=["Gold", "Silver", "Bronze", "Participations"], ascending=False, inplace=True
    )

    return df.head(top)


def get_by_contestant(name):
    data = get_all_contests()
    return data[data["Name"] == name].reset_index(drop=True)


def get_contestants_name(country=None):
    if country is None:
        data = get_all_contests()
    else:
        data = get_by_country(country)
    return data["Name"].unique().tolist()
