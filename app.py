from flask import Flask, render_template, request, redirect, url_for, flash
import os
from flask import send_file
from reports.report_generator import generate_pdf
from reports.excel_generator import generate_excel
from analysis.data_loader import load_dataset
from analysis.kpi import calculate_kpis
from analysis.charts import get_monthly_sales, get_category_sales
from analysis.analytics import (
    region_sales,
    category_profit,
    top_products,
    top_customers
)

app = Flask(__name__)
app.secret_key = "retail_dashboard_secret"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"csv"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ===================================================
# Dashboard
# ===================================================

@app.route("/")
def dashboard():

    df = load_dataset()

    kpis = calculate_kpis(df)

    sales_labels, sales_values = get_monthly_sales(df)
    category_labels, category_values = get_category_sales(df)

    upload_path = os.path.join(app.config["UPLOAD_FOLDER"], "current_dataset.csv")

    if os.path.exists(upload_path):
        dataset_name = "current_dataset.csv"
    else:
        dataset_name = "Superstore.csv"

    return render_template(
        "dashboard.html",

        total_sales=kpis["total_sales"],
        total_profit=kpis["total_profit"],
        total_orders=kpis["total_orders"],
        total_customers=kpis["total_customers"],
        total_quantity=kpis["total_quantity"],

        sales_labels=sales_labels,
        sales_values=sales_values,

        category_labels=category_labels,
        category_values=category_values,

        dataset_name=dataset_name
    )


# ===================================================
# Analytics
# ===================================================

@app.route("/analytics")
def analytics():

    df = load_dataset()

    region = region_sales(df)
    category = category_profit(df)

    products = top_products(df)
    customers = top_customers(df)

    return render_template(
        "analytics.html",

        region_labels=region["labels"],
        region_values=region["values"],

        category_labels=category["labels"],
        category_values=category["values"],

        products=products.to_dict("records"),
        customers=customers.to_dict("records")
    )


# ===================================================
# Upload Dataset
# ===================================================

@app.route("/upload", methods=["POST"])
def upload_dataset():

    if "dataset" not in request.files:
        flash("No file selected!")
        return redirect(url_for("dashboard"))

    file = request.files["dataset"]

    if file.filename == "":
        flash("Please choose a CSV file.")
        return redirect(url_for("dashboard"))

    if file and allowed_file(file.filename):

        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            "current_dataset.csv"
        )

        file.save(filepath)

        flash("Dataset uploaded successfully!")

    else:
        flash("Only CSV files are allowed.")

    return redirect(url_for("dashboard"))

@app.route("/download-pdf")
def download_pdf():

    df = load_dataset()

    kpis = calculate_kpis(df)

    pdf = generate_pdf(kpis)

    return send_file(
        pdf,
        as_attachment=True
    )


# ===================================================
# Run App
# ===================================================
@app.route("/reports")
def reports():

    upload_path = os.path.join(app.config["UPLOAD_FOLDER"], "current_dataset.csv")

    if os.path.exists(upload_path):
        dataset_name = "current_dataset.csv"
    else:
        dataset_name = "Superstore.csv"

    return render_template(
        "reports.html",
        dataset_name=dataset_name
    )
from flask import send_file

@app.route("/download/excel")
def download_excel():

    df = load_dataset()

    excel_path = generate_excel(df)

    return send_file(
        excel_path,
        as_attachment=True
    )
if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)
    