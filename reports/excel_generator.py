import os
import pandas as pd

from analysis.kpi import calculate_kpis
from analysis.analytics import (
    region_sales,
    category_profit,
    top_products,
    top_customers
)


def generate_excel(df):

    os.makedirs("generated_reports", exist_ok=True)

    filename = "generated_reports/Retail_Report.xlsx"

    kpis = calculate_kpis(df)

    with pd.ExcelWriter(filename, engine="openpyxl") as writer:

        # ================= Dashboard Summary =================

        summary = pd.DataFrame({

            "Metric": [

                "Total Sales",
                "Total Profit",
                "Total Orders",
                "Total Customers",
                "Quantity Sold"

            ],

            "Value": [

                kpis["total_sales"],
                kpis["total_profit"],
                kpis["total_orders"],
                kpis["total_customers"],
                kpis["total_quantity"]

            ]

        })

        summary.to_excel(
            writer,
            sheet_name="Dashboard Summary",
            index=False
        )

        # ================= Original Dataset =================

        df.to_excel(
            writer,
            sheet_name="Original Dataset",
            index=False
        )

        # ================= Top Products =================

        top_products(df).to_excel(
            writer,
            sheet_name="Top Products",
            index=False
        )

        # ================= Top Customers =================

        top_customers(df).to_excel(
            writer,
            sheet_name="Top Customers",
            index=False
        )

        # ================= Category Analysis =================

        category = pd.DataFrame({

            "Category": category_profit(df)["labels"],
            "Profit": category_profit(df)["values"]

        })

        category.to_excel(
            writer,
            sheet_name="Category Analysis",
            index=False
        )

        # ================= Region Analysis =================

        region = pd.DataFrame({

            "Region": region_sales(df)["labels"],
            "Sales": region_sales(df)["values"]

        })

        region.to_excel(
            writer,
            sheet_name="Region Analysis",
            index=False
        )

        # ================= AI Insights =================

        insights = pd.DataFrame({

            "Business Insights": [

                "Highest revenue categories can be identified from Category Analysis.",
                "Top Customers sheet lists the highest-value customers.",
                "Top Products sheet identifies the best-selling products.",
                "Dashboard Summary provides overall KPIs.",
                "This report is automatically generated using Flask + Pandas."

            ]

        })

        insights.to_excel(
            writer,
            sheet_name="AI Insights",
            index=False
        )

    return filename