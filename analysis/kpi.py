def calculate_kpis(df):

    total_sales = round(df["sales"].sum(), 2)

    total_profit = round(df["profit"].sum(), 2)

    total_orders = df["order_id"].nunique()

    total_customers = df["customer_id"].nunique()

    total_quantity = int(df["quantity"].sum())

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "total_quantity": total_quantity
    }