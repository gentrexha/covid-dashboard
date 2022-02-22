#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime as dt
from datetime import date, timedelta
import numpy as np
import pycountry


DATASET_FILTERS = ["Confirmed", "Recovered", "Deaths"]

DATASET_OPTIONS = [
    {"label": dataset_filter, "value": dataset_filter}
    for dataset_filter in DATASET_FILTERS
]


def return_wanted_dataset(
    covid_confirmed, covid_deaths, covid_recovered, dataset_types
):
    ds = covid_confirmed
    if dataset_types == "Deaths":
        ds = covid_deaths
    elif dataset_types == "Recovered":
        ds = covid_recovered
    return ds


def filter_dataframe(df, continent_types, date_picker):
    dp_value = dt.strptime(date_picker, "%Y-%m-%d")
    day = str(dp_value.day)
    month = str(dp_value.month)
    year = str(dp_value.year)

    if day[0] == "0":
        day = day[1 : len(day)]
    if month[0] == "0":
        month = month[1 : len(month)]

    picked_date = str(month) + "/" + str(day) + "/" + str(year)[2:]

    if continent_types == "All" or continent_types is None:
        dff = df[
            [
                "Country/Region",
                "population",
                "continent",
                "gdp_per_capita",
                "iso_code",
                # "ISO",
                # "Tests",
                # "Color",
                picked_date,
            ]
        ]
        return dff, picked_date
    else:
        dff = df[
            [
                "Country/Region",
                "population",
                "continent",
                "gdp_per_capita",
                "iso_code",
                # "ISO",
                # "Tests",
                # "Color",
                picked_date,
            ]
        ]
        dff = dff[dff["continent"] == continent_types]
        return dff, picked_date


def drop_non_dates(df_to_be_dropped: pd.DataFrame) -> pd.DataFrame:
    dff = df_to_be_dropped.drop(
        ["location", "continent", "gdp_per_capita", "population", "iso_code"],
        axis=1,
    )
    return dff


def find_iso_code(country: str):
    if country == "US":
        return "USA"
    try:
        obj_country = pycountry.countries.search_fuzzy(country)
    except:
        return np.nan
    if obj_country[0].alpha_3 is not None:
        return obj_country[0].alpha_3
    else:
        return np.nan


def set_country(province: str, country: str):
    if province is np.nan:
        return country
    else:
        return province


def setup_data():
    df_tests = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
    df_tests = df_tests.loc[
        df_tests["date"] == f"{date.today()-timedelta(days=2)}"
    ].reset_index(drop=True)
    df_tests = df_tests[
        ["location", "continent", "gdp_per_capita", "population", "iso_code"]
    ]
    # Total
    total = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
        "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    )
    # Recovered
    recovered = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
        "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
    )
    # Deaths
    deaths = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
        "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    )

    # country
    total["country"] = total.apply(
        lambda x: set_country(x["Province/State"], x["Country/Region"]), axis=1
    )

    for df in [recovered, total, deaths]:
        df.drop(["Province/State", "Lat", "Long"], axis=1, inplace=True)

    # Iso-codes
    total["iso_code"] = total.apply(lambda x: find_iso_code(x["country"]), axis=1)
    total = total.drop("country", axis=1)
    recovered["iso_code"] = total["iso_code"]
    deaths["iso_code"] = total["iso_code"]

    # Joining extra data and storing data
    df_deaths = pd.merge(deaths, df_tests, how="left", on="iso_code")
    df_recovered = pd.merge(recovered, df_tests, how="left", on="iso_code")
    df_total = pd.merge(total, df_tests, how="left", on="iso_code")

    return df_deaths, df_recovered, df_total


def main():
    """ Main program """
    setup_data()
    return 0


if __name__ == "__main__":
    main()
