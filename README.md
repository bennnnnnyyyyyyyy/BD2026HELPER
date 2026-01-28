# 🏥 Ben's DME Data Hub

> **A professional suite for DME outreach, NPI enrichment, and advanced data management.**  
> *Built for speed, industrial aesthetics, and robust local processing.*

---

## 🚀 Quick Start

1.  **Open Dashboard**: Double-click **`homepage.html`**.
2.  **Basic Tools**: Launch the Power Dialer or Search Engine directly from the cards.
3.  **Advanced Tools (NPI Hub)**: 
    - Open a terminal in the folder containing `npi_hub.py`.
    - Run: `python npi_hub.py`
    - Click **"Launch NPI Hub"** on the dashboard.

---

## 🛠️ The Toolkit

### 1. 📞 Power Dialer (`dialer.html`)
A high-velocity calling interface designed for sales efficiency.
-   **CSV Import**: Drag & drop your lead list.
-   **Smart Mapping**: Auto-identifies `AuthPhone`, `Legalbusinessname`, and `Comments`.
-   **Disposition Logging**: One-click updates for **VM**, **GK**, **NA**, **WN**, or **Notes**.
-   **History**: Appends timestamped notes to existing comments.

### 2. 📊 NPI Data Enrichment
Bulk enrich your lead lists using local reference data.
-   **Matching Logic**: Matches by NPI, Name + State, or Phone.
-   **Automated**: Populates `AuthOfficialName`, `AuthPhone`, and `NPI` instantly.

### 3. 🔍 NPI Search Engine
A blazing-fast search interface for exploring the NPPES registry.
-   **Instant Filter**: Search thousands of records as you type.
-   **Advanced View**: Detailed modal views for every provider.
-   **Export**: Quick export to CSV/JSON format.

### 4. 🛠️ NPI Tool Hub (`npi_hub.py`)
A unified backend suite for heavy data processing.
-   **Background Processing**: Handles massive CSVs without freezing your browser.
-   **NPPES Extraction**: Filters millions of records directly from the NPPES ZIP file.
-   **Multi-CSV Merger**: Combines lead lists and removes duplicates safely.
-   **Sheet Formatter**: Prepares data for seamless Google Sheets upload.

---

## 📂 File Structure

-   **`homepage.html`**: The central dashboard hub.
-   **`dialer.html`**: Standalone calling application.
-   **`npi_hub.py`**: Flask backend server for advanced tools.
-   **`templates/index.html`**: NPI Hub interface.
-   **`README.md`**: This guide.

---

## 💡 Pro Tips

-   **Local & Secure**: All processing happens on your machine. No data is sent to external servers.
-   **Requirements**: The NPI Hub requires Python (with `flask` and `pandas` installed).
-   **Save Progress**: Periodically export your CSVs in the Dialer to ensure your work is saved.

---

*internal use only • v2.2.0 • 2026*
