# 📊 Automated Financial Pipeline & Analytics Dashboard

An end-to-end Python solution for automated invoice generation, hybrid data extraction (PDF/Excel), and real-time business intelligence.

## 🚀 Project Overview
This project solves the "manual data entry" problem for small businesses. It provides a self-sustaining pipeline that:
1. **Generates** professional PDF invoices from raw data.
2. **Extracts** financial data from mixed sources (PDF & Excel) using Regex and OCR logic.
3. **Validates** data integrity with an accessibility layer (Dual-tone audio alerts).
4. **Visualizes** financial health through high-contrast automated charts.

## 🛠️ Tech Stack
- **Python 3.x**: Core logic.
- **Pandas**: Data manipulation and Master Tracker management.
- **PDFPlumber/FPDF**: PDF extraction and generation.
- **Matplotlib/Seaborn**: High-contrast data visualization.
- **Streamlit**: (Optional) No-code web interface for client uploads.

## 📁 Key Features
- **Hybrid Sync**: Processes `.pdf` and `.xlsx` files simultaneously from a single watch-folder.
- **Accessibility Layer**: Engineered for users with hardware limitations (e.g., damaged monitors) using `winsound` audio-coded feedback:
  - 🔊 **High Pitch (1000Hz)**: Successful sync.
  - 🔉 **Low Pitch (300Hz)**: Warning! Data integrity issue (e.g., $0.00 amount detected).
- **Status Automation**: Automatically categorizes invoices as **Paid, Pending, OVERDUE, or Partial**.

## 📈 Visual Reports
The system automatically generates two high-impact visuals:
- **Bar Chart**: Total revenue volume by status.
- **Pie Chart**: Percentage distribution of financial health.

## 📝 How to Use
1. Place PDF or Excel invoices in the `/To_Process` folder.
2. Run `python automation.py`.
3. Review the updated `invoice_summary.csv` and the generated `.png` charts.

---
*Developed as a high-speed, accessible financial automation tool.*