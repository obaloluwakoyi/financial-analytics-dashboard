# make_pdf.py
from fpdf import FPDF
import matplotlib
matplotlib.use("Agg")  # REQUIRED for Docker / headless
import matplotlib.pyplot as plt
import tempfile
import shutil
import os
import pandas as pd


REQUIRED_COLUMNS = {"Invoice", "Client", "Amount", "Status"}


class ReportError(Exception):
    pass


def _validate_df(df: pd.DataFrame):
    if df.empty:
        raise ReportError("Cannot generate report from empty dataset")

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ReportError(f"Missing required columns: {missing}")

    if not pd.api.types.is_numeric_dtype(df["Amount"]):
        raise ReportError("Amount column must be numeric")


def _render_chart(df: pd.DataFrame, path: str):
    grouped = df.groupby("Status")["Amount"].sum()
    if grouped.empty:
        raise ReportError("No data available for chart rendering")

    plt.figure(figsize=(6, 4))
    grouped.plot(kind="pie", autopct="%1.1f%%", startangle=90)
    plt.title("Revenue Distribution by Status")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def _add_table(pdf: FPDF, df: pd.DataFrame):
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Audit Table - All Transactions", ln=True)
    pdf.ln(3)

    headers = [("Invoice", 40), ("Client", 70), ("Amount", 40), ("Status", 40)]

    pdf.set_font("Arial", "B", 9)
    for h, w in headers:
        pdf.cell(w, 8, h, 1)
    pdf.ln()

    pdf.set_font("Arial", size=8)

    for _, row in df.iterrows():
        if pdf.get_y() > 260:  # pagination guard
            pdf.add_page()
            pdf.set_font("Arial", "B", 9)
            for h, w in headers:
                pdf.cell(w, 8, h, 1)
            pdf.ln()
            pdf.set_font("Arial", size=8)

        pdf.cell(40, 7, str(row["Invoice"]), 1)
        pdf.cell(70, 7, str(row["Client"])[:35], 1)
        pdf.cell(40, 7, f"${row['Amount']:,.2f}", 1)
        pdf.cell(40, 7, str(row["Status"]), 1)
        pdf.ln()


def create_report(df: pd.DataFrame) -> bytes:
    _validate_df(df)

    tmpdir = tempfile.mkdtemp()
    try:
        chart_path = os.path.join(tmpdir, "revenue.png")
        _render_chart(df, chart_path)

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Title
        pdf.set_font("Arial", "B", 20)
        pdf.cell(0, 15, "Executive Financial Report", ln=True, align="C")
        pdf.ln(8)

        # Summary
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Total Portfolio Value: ${df['Amount'].sum():,.2f}", ln=True)
        pdf.cell(0, 10, f"Total Invoices Processed: {len(df)}", ln=True)
        pdf.ln(5)

        pdf.image(chart_path, x=30, w=150)

        # Table
        pdf.add_page()
        _add_table(pdf, df)

        return pdf.output(dest="S").encode("latin-1", "replace")

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)