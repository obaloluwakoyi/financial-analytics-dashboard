import streamlit as st
import pandas as pd
import tempfile
import os
from database import get_engine, init_db, save_invoices, load_invoices
from automation import process_excel, process_pdf
from make_pdf import create_report
from logger import setup_logging, get_logger

# Initialize environment (once per session via cache)
setup_logging()
logger = get_logger("dashboard")

# FIX 1: Cache the engine so it's not recreated on every Streamlit rerun
@st.cache_resource
def get_db_engine():
    engine = get_engine()
    init_db(engine)
    return engine

engine = get_db_engine()

st.set_page_config(page_title="Financial App", layout="wide")
st.title("📊 Executive Financial Dashboard")

# --- Sidebar: File Ingestion ---
st.sidebar.header("Data Ingestion")
uploaded_file = st.sidebar.file_uploader("Upload Invoice (Excel or PDF)", type=["xlsx", "pdf"])

if uploaded_file:
    # FIX 2: Use session_state to avoid reprocessing the same file on every rerun
    file_id = f"{uploaded_file.name}_{uploaded_file.size}"
    if st.session_state.get("last_processed") != file_id:
        # FIX 3: Save temp file to /tmp (not cwd) and clean up after use
        suffix = ".xlsx" if uploaded_file.name.lower().endswith(".xlsx") else ".pdf"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name

        try:
            with st.sidebar.spinner("Processing file..."):
                if suffix == ".xlsx":
                    df_new = process_excel(tmp_path)
                else:
                    df_new = process_pdf(tmp_path)

            # Standardize columns to match DB schema
            df_db = df_new.rename(columns={
                "Invoice": "invoice", "Client": "client",
                "Amount": "amount", "Date": "date",
                "Status": "status", "Source File": "source"
            })

            save_invoices(df_db, engine)
            st.session_state["last_processed"] = file_id
            st.sidebar.success(f"✅ Processed: {uploaded_file.name}")
            logger.info("Processed file: %s", uploaded_file.name)

        except Exception as e:
            logger.error("Failed to process %s: %s", uploaded_file.name, e)
            st.sidebar.error(f"❌ Error: {e}")

        finally:
            # FIX 3 cont: Always clean up the temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    else:
        st.sidebar.info("File already processed.")

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
    report_df = data.rename(columns={
        "invoice": "Invoice", "client": "Client",
        "amount": "Amount", "status": "Status"
    })

    if st.button("Generate Executive PDF"):
        try:
            with st.spinner("Generating report..."):
                pdf_bytes = create_report(report_df)
            # FIX 4: download_button must be called outside the if-button block
            # to avoid it disappearing immediately. Use session_state to hold bytes.
            st.session_state["pdf_bytes"] = pdf_bytes
        except Exception as e:
            st.error(f"❌ PDF generation failed: {e}")

    # FIX 4: Render download button persistently once PDF is ready
    if "pdf_bytes" in st.session_state:
        st.download_button(
            label="⬇️ Download PDF Report",
            data=st.session_state["pdf_bytes"],
            file_name="financial_report.pdf",
            mime="application/pdf",
        )
else:
    st.info("No data found in the database. Please upload a file via the sidebar.")
