import pandas as pd


def get_monthly_sales(df):

    df["order_date"] = pd.to_datetime(df["order_date"])

    df["month"] = df["order_date"].dt.strftime("%b")

    month_order = [
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
    ]

    monthly = (
        df.groupby("month")["sales"]
        .sum()
        .reindex(month_order, fill_value=0)
    )

    return monthly.index.tolist(), monthly.values.tolist()


def get_category_sales(df):

    category = (
        df.groupby("category")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    return category.index.tolist(), category.values.tolist()