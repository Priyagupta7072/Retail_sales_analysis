import pandas as pd


def region_sales(df):

    if "region" not in df.columns or "sales" not in df.columns:
        return {"labels": [], "values": []}

    data = (
        df.groupby("region")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "labels": data.index.tolist(),
        "values": data.values.tolist()
    }


def category_profit(df):

    if "category" not in df.columns or "profit" not in df.columns:
        return {"labels": [], "values": []}

    data = (
        df.groupby("category")["profit"]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "labels": data.index.tolist(),
        "values": data.values.tolist()
    }


def top_products(df):

    if "product_name" not in df.columns or "sales" not in df.columns:
        return pd.DataFrame(columns=["product_name", "sales"])

    data = (
        df.groupby("product_name")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    return data


def top_customers(df):

    if "customer_name" not in df.columns or "sales" not in df.columns:
        return pd.DataFrame(columns=["customer_name", "sales"])

    data = (
        df.groupby("customer_name")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    return data