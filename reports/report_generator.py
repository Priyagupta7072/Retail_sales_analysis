from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
import datetime
import os


def generate_pdf(kpis):

    os.makedirs("generated_reports", exist_ok=True)

    filename = "generated_reports/Retail_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER

    heading = styles["Heading2"]
    normal = styles["BodyText"]

    story = []

    # Title
    story.append(Paragraph("Retail Sales Analysis Report", title))
    story.append(Spacer(1, 20))

    # Date
    story.append(
        Paragraph(
            f"<b>Generated On:</b> {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}",
            normal
        )
    )

    story.append(Spacer(1, 20))

    story.append(Paragraph("Business KPI Summary", heading))
    story.append(Spacer(1, 10))

    data = [
        ["Metric", "Value"],
        ["Total Sales", f"${kpis['total_sales']:,.2f}"],
        ["Total Profit", f"${kpis['total_profit']:,.2f}"],
        ["Total Orders", str(kpis["total_orders"])],
        ["Total Customers", str(kpis["total_customers"])],
        ["Quantity Sold", str(kpis["total_quantity"])]
    ]

    table = Table(data, colWidths=[220, 180])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F46E5")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 1, colors.grey),

        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        ("TOPPADDING", (0, 1), (-1, -1), 8),
    ]))

    story.append(table)

    story.append(Spacer(1, 25))

    story.append(Paragraph("Business Insights", heading))

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "• This report is automatically generated from the uploaded retail dataset.",
            normal
        )
    )

    story.append(
        Paragraph(
            "• KPI values update whenever a new dataset is uploaded.",
            normal
        )
    )

    story.append(
        Paragraph(
            "• This dashboard has been developed using Python, Flask and Pandas.",
            normal
        )
    )

    story.append(Spacer(1, 30))

    story.append(
        Paragraph(
            "<b>End of Report</b>",
            normal
        )
    )

    doc.build(story)

    return filename