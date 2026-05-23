# automation.py
import os
import re
import pandas as pd
import pdfplumber
from datetime import datetime
from typing import Optional

CANONICAL = ["Invoice", "Client", "Amount", "Date", "Status", "Source File"]


class AutomationError(Exception):
    pass


def normalize_dataframe(df: pd.DataFrame, source: str) -> pd.DataFrame:
    df.columns = [c.strip().lower() for c in df.columns]

    def pick(*names):
        for n in names:
            if n in df.columns:
                return df[n]
        return None

    out = pd.DataFrame({
        "Invoice": pick("invoice", "invoice number"),
        "Client": pick("client", "customer"),
        "Amount": pd.to_numeric(
            pick("amount", "total amount"),
            errors="coerce"
        ),
        "Date": pick("date", "invoice date"),
        "Status": pick("status"),
        "Source File": source,
    })

    out["Amount"] = out["Amount"].fillna(0)
    out = out.fillna("")

    return out[CANONICAL]


def process_excel(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise AutomationError(f"Excel file not found: {path}")

    try:
        df = pd.read_excel(path, engine="openpyxl")
        if df.empty:
            raise AutomationError("Excel file is empty")

        return normalize_dataframe(df, os.path.basename(path))

    except Exception as e:
        raise AutomationError(f"Excel processing failed: {path}") from e


def extract_from_pdf(text: str) -> dict:
    patterns = {
        "Invoice": r"(invoice\s*(number)?[:\s]*)?([\w\-]+)",
        "Amount": r"(total|amount)\s*[:\$]?\s*([\d,\.]+)",
        "Date": r"(date)\s*[:\s]*([\d\-\/]+)",
    }

    def match(p):
        m = re.search(p, text, re.I)
        return m.group(m.lastindex) if m else ""

    amount = match(patterns["Amount"])
    amount = float(amount.replace(",", "")) if amount else 0

    return {
        "Invoice": match(patterns["Invoice"]),
        "Client": "",
        "Amount": amount,
        "Date": match(patterns["Date"]),
        "Status": "",
    }


def process_pdf(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise AutomationError(f"PDF not found: {path}")

    try:
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

        if not text.strip():
            raise AutomationError("PDF contains no extractable text")

        data = extract_from_pdf(text)
        data["Source File"] = os.path.basename(path)

        return pd.DataFrame([data], columns=CANONICAL)

    except Exception as e:
        raise AutomationError(f"PDF processing failed: {path}") from e