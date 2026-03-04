import streamlit as st
import pandas as pd
from database import get_engine, init_db, save_invoices, load_invoices
from automation import process_excel, process_pdf
from make_pdf import create_report
from logger import setup_logging, get_logger

# Initialize environment
setup_logging()
logger = get_logger("dashboard")
engine = get_engine()
init_db(engine)

st.set_page_config(page_title="Financial App", layout="wide")
st.title("📊 Executive Financial Dashboard")

# --- Sidebar: File Ingestion ---
st.sidebar.header("Data Ingestion")
uploaded_file = st.sidebar.file_uploader("Upload Invoice (Excel or PDF)", type=["xlsx", "pdf"])

if uploaded_file:
    # Save temp file for processing
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        if uploaded_file.name.endswith(".xlsx"):
            df_new = process_excel(uploaded_file.name)
        else:
            df_new = process_pdf(uploaded_file.name)
        
        # Standardize columns to match DB schema (invoice, client, amount, date, status, source)
        df_db = df_new.rename(columns={"Invoice": "invoice", "Client": "client", 
                                       "Amount": "amount", "Date": "date", 
                                       "Status": "status", "Source File": "source"})
        
        save_invoices(df_db, engine)
        st.sidebar.success(f"Processed: {uploaded_file.name}")
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

# --- Main View: Data & Reporting ---
data = load_invoices(engine)

if not data.empty:
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${data['amount'].sum():,.2f}")
    col2.metric("Total Invoices", len(data))
    col3.metric("Unique Clients", data['client'].nunique())

    # Data Table
    st.subheader("Transaction History")
    st.dataframe(data, use_container_width=True)

    # Export Logic
    st.subheader("Reporting")
    # Convert DB columns back to Report expected names
    report_df = data.rename(columns={"invoice": "Invoice", "client": "Client", 
                                     "amount": "Amount", "status": "Status"})
    
    if st.button("Generate Executive PDF"):
        pdf_bytes = create_report(report_df)
        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name="financial_report.pdf",
            mime="application/pdf"
        )
else:
    st.info("No data found in the database. Please upload a file via the sidebar.")