"""
filters.py — Data loading, cleaning, merging, and filter functions
for the Wine Reviews Dashboard.
"""

import pandas as pd
import numpy as np
import streamlit as st


@st.cache_data(show_spinner="Loading & merging wine data...")
def load_and_merge_data():
    """
    Load both CSV files, merge them, clean the result.
    Returns a single cleaned DataFrame.
    """
    df1 = pd.read_csv("data/winemag-data_first150k.csv", index_col=0)
    df2 = pd.read_csv("data/winemag-data-130k-v2.csv", index_col=0)

    # Union both datasets (df1 missing taster_name, taster_twitter_handle, title)
    df = pd.concat([df1, df2], ignore_index=True, sort=False)

    # Drop exact duplicate rows
    df.drop_duplicates(inplace=True)

    # Clean numeric columns
    df["points"] = pd.to_numeric(df["points"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Strip whitespace from string columns
    str_cols = ["country", "description", "designation", "province",
                "region_1", "region_2", "variety", "winery",
                "taster_name", "taster_twitter_handle", "title"]
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace(["nan", "None", ""], np.nan)

    df.reset_index(drop=True, inplace=True)
    return df


def get_filter_options(df):
    """Return unique sorted values for dropdown filters."""
    countries = sorted(df["country"].dropna().unique().tolist())
    varieties = sorted(df["variety"].dropna().unique().tolist())
    provinces = sorted(df["province"].dropna().unique().tolist())
    wineries = sorted(df["winery"].dropna().unique().tolist())

    points_min = int(df["points"].min()) if df["points"].notna().any() else 80
    points_max = int(df["points"].max()) if df["points"].notna().any() else 100
    price_min = float(df["price"].min()) if df["price"].notna().any() else 0.0
    price_max = float(df["price"].max()) if df["price"].notna().any() else 3300.0

    return {
        "countries": countries,
        "varieties": varieties,
        "provinces": provinces,
        "wineries": wineries,
        "points_range": (points_min, points_max),
        "price_range": (price_min, price_max),
    }


def apply_filters(df, filters_dict):
    """
    Apply all active filters to the DataFrame.
    filters_dict keys:
        - selected_countries: list
        - selected_varieties: list
        - points_range: tuple (min, max)
        - price_range: tuple (min, max)
        - search_text: str
    Returns filtered DataFrame.
    """
    filtered = df.copy()

    # Country filter
    if filters_dict.get("selected_countries"):
        filtered = filtered[filtered["country"].isin(filters_dict["selected_countries"])]

    # Variety filter
    if filters_dict.get("selected_varieties"):
        filtered = filtered[filtered["variety"].isin(filters_dict["selected_varieties"])]

    # Points range slider
    if filters_dict.get("points_range"):
        pmin, pmax = filters_dict["points_range"]
        filtered = filtered[
            (filtered["points"] >= pmin) & (filtered["points"] <= pmax)
        ]

    # Price range slider
    if filters_dict.get("price_range"):
        prmin, prmax = filters_dict["price_range"]
        filtered = filtered[
            (filtered["price"] >= prmin) & (filtered["price"] <= prmax)
        ]

    # Text search in description
    if filters_dict.get("search_text"):
        keyword = filters_dict["search_text"].lower()
        filtered = filtered[
            filtered["description"]
            .astype(str)
            .str.lower()
            .str.contains(keyword, na=False)
        ]

    return filtered
