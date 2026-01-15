# 🏥 Ben's DME Data Hub

> **A professional, standalone suite for DME outreach, NPI enrichment, and data management.**  
> *Built for speed, privacy, and zero-setup deployment.*

---

## 🚀 Quick Start

1.  **Download** the entire folder.
2.  Double-click **`homepage.html`**.
3.  That's it! Access all tools from the dashboard.

---

## 🛠️ The Toolkit

### 1. 📞 Power Dialer (`dialer.html`)
A high-velocity calling interface designed for sales teams.
-   **CSV Import**: Drag & drop your lead list.
-   **Smart Mapping**: Automatically finds columns like `AuthPhone`, `Legalbusinessname`, and `Comments`.
-   **Disposition Buttons**: One-click logging for **VM**, **GK**, **NA**, **WN**, or **Custom Notes**.
-   **History Tracking**: Appends new notes to existing comments with timestamps (e.g., `VM - Left msg (1/15/2026)`).
-   **Export**: Saves your work to a new CSV with full history.

### 2. 📊 NPI Data Enrichment
Bulk enrich your lead lists using a master NPPES database file.
-   **Offline Processing**: Uses a local reference file (no API limits).
-   **Matching Logic**: Matches by **NPI**, **Name + State**, or **Phone Number**.
-   **Fills Gaps**: Automatically populates `AuthOfficialName`, `AuthPhone`, and `NPI`.

### 3. 🔍 NPI Search Engine
A real-time, blazing fast search interface for the NPPES database.
-   **Instant Search**: Type to filter thousands of records instantly.
-   **Advanced Filters**: Filter by State, Taxonomy, or Missing Info.
-   **Export**: Select specific rows and export to CSV/JSON.
-   **Portability**: Integrated directly into the homepage—no extra tabs needed.

---

## 📂 File Structure

-   **`homepage.html`**: The main entry point. Contains the Dashboard, Enrichment Tool, and Search Engine.
-   **`dialer.html`**: The standalone calling application (launchable from homepage).
-   **`README.md`**: This file.

---

## 💡 Pro Tips

-   **Privacy First**: All data processing happens **locally** in your browser. No data is ever sent to a server.
-   **Performance**: For best results in the Search/Enrichment tools, ensure your computer has enough RAM to handle large CSVs.
-   **Save Often**: When using the Dialer, export your CSV periodically to save your progress.

---

*internal use only • v2.1.0 • 2026*
