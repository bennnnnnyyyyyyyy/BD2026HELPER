import os
import csv
import zipfile
import json
import threading
import time
from datetime import datetime
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_file, Response

app = Flask(__name__)

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Default paths from user's scripts
ZIP_FILENAME = "NPPES_Data_Dissemination_December_2025.zip"
EXTRACT_DIR = "NPPES_Data_Dissemination_December_2025"

# --- Global State for Progress Tracking ---
# Each task (filter, merge, format) will share its progress here
progress_state = {
    'status': 'idle',  # idle, processing, complete, error
    'percent': 0,
    'message': '',
    'log': [],
    'result_file': None
}

def update_progress(percent, message, append_log=True):
    progress_state['percent'] = percent
    progress_state['message'] = message
    if append_log:
        log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
        progress_state['log'].append(log_entry)
        print(log_entry)

# --- Integrated Core Logic ---

def find_main_csv(folder):
    csv_files = [f for f in os.listdir(folder) if f.endswith(".csv") and "FileHeader" not in f]
    return os.path.join(folder, csv_files[0]) if csv_files else None

def filter_task(state, update_start, update_end, enum_start, enum_end, taxonomies):
    try:
        progress_state['status'] = 'processing'
        progress_state['log'] = []
        progress_state['percent'] = 0
        
        # 1. Extraction
        if not os.path.exists(EXTRACT_DIR):
            update_progress(5, f"Extracting {ZIP_FILENAME}...")
            if not os.path.exists(ZIP_FILENAME):
                raise FileNotFoundError(f"ZIP file '{ZIP_FILENAME}' not found!")
            
            with zipfile.ZipFile(ZIP_FILENAME, 'r') as zip_ref:
                files = zip_ref.namelist()
                total_files = len(files)
                for i, file in enumerate(files):
                    zip_ref.extract(file, EXTRACT_DIR)
                    if i % max(1, total_files // 10) == 0:
                        update_progress(5 + int((i/total_files) * 15), f"Extracting {file}...")
        
        csv_path = find_main_csv(EXTRACT_DIR)
        if not csv_path:
            raise FileNotFoundError("Main data CSV file not found in extraction directory.")
        
        update_progress(20, f"Using data file: {os.path.basename(csv_path)}")

        # 2. Date Parsing Setup
        def parse_date(d_str):
            return datetime.strptime(d_str, "%m/%d/%Y").date() if d_str else None

        u_start = parse_date(update_start)
        u_end = parse_date(update_end)
        e_start = parse_date(enum_start)
        e_end = parse_date(enum_end)
        tax_list = [t.strip() for t in taxonomies.split(',')] if taxonomies else []

        # 3. Filtering
        output_name = f"filtered_nppes_{state or 'all'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        output_path = os.path.join(BASE_DIR, output_name)
        
        # Count rows for progress (quick estimation)
        update_progress(25, "Estimating rows...")
        file_size = os.path.getsize(csv_path)
        
        matched_rows = 0
        with open(csv_path, newline='', encoding='utf-8') as infile, \
             open(output_path, 'w', newline='', encoding='utf-8') as outfile:
            
            reader = csv.DictReader(infile)
            writer = None
            
            # Use chunks for progress updates
            processed_bytes = 0
            for row in reader:
                # Filter Logic
                # State
                if state:
                    mailing_s = row.get('Provider Business Mailing Address State Name', '').strip().upper()
                    practice_s = row.get('Provider Business Practice Location Address State Name', '').strip().upper()
                    if state.upper() not in [mailing_s, practice_s]:
                        continue
                
                # Last Update Date
                if u_start or u_end:
                    l_upd = row.get('Last Update Date', '').strip()
                    try:
                        rd = datetime.strptime(l_upd, "%m/%d/%Y").date()
                        if u_start and rd < u_start: continue
                        if u_end and rd > u_end: continue
                    except: continue

                # Enumeration Date
                if e_start or e_end:
                    enum_d = row.get('Provider Enumeration Date', '').strip()
                    try:
                        rd = datetime.strptime(enum_d, "%m/%d/%Y").date()
                        if e_start and rd < e_start: continue
                        if e_end and rd > e_end: continue
                    except: continue

                # Taxonomy
                if tax_list:
                    match = False
                    for i in range(1, 15):
                        t_code = row.get(f'Healthcare Provider Taxonomy Code_{i}', '').strip()
                        if t_code in tax_list:
                            match = True
                            break
                    if not match: continue

                # Write Match
                if writer is None:
                    writer = csv.DictWriter(outfile, fieldnames=row.keys())
                    writer.writeheader()
                writer.writerow(row)
                matched_rows += 1
                
                # Progress update every 10,000 rows
                if matched_rows % 10000 == 0:
                    update_progress(25 + int((matched_rows / 1000000) * 50) % 70, f"Found {matched_rows:,} matches...")

        progress_state['status'] = 'complete'
        progress_state['result_file'] = output_name
        update_progress(100, f"SUCCESS! Saved {matched_rows:,} records to {output_name}")

    except Exception as e:
        progress_state['status'] = 'error'
        update_progress(0, f"ERROR: {str(e)}")

def merge_task(file1, file2):
    try:
        progress_state['status'] = 'processing'
        progress_state['log'] = []
        update_progress(10, f"Loading {file1}...")
        df1 = pd.read_csv(file1, dtype=str, low_memory=False)
        update_progress(40, f"Loading {file2}...")
        df2 = pd.read_csv(file2, dtype=str, low_memory=False)
        
        update_progress(70, "Merging and removing duplicates...")
        combined = pd.concat([df1, df2], ignore_index=True)
        deduped = combined.drop_duplicates(subset=['NPI'], keep='first')
        
        output_name = f"MERGED_NPI_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        update_progress(90, f"Saving to {output_name}...")
        deduped.to_csv(output_name, index=False)
        
        progress_state['status'] = 'complete'
        progress_state['result_file'] = output_name
        update_progress(100, f"Done! Merged {len(deduped):,} unique records.")
    except Exception as e:
        progress_state['status'] = 'error'
        update_progress(0, f"ERROR: {str(e)}")

def format_task(input_file):
    try:
        progress_state['status'] = 'processing'
        progress_state['log'] = []
        update_progress(10, f"Loading {input_file} for formatting...")
        
        column_mapping = {
            'Last Update Date': 'UpdateDate',
            'Provider Organization Name (Legal Business Name)': 'Legalbusinessname',
            'Provider Business Practice Location Address State Name': 'State',
            'Provider Business Practice Location Address Telephone Number': 'OfficePhone',
            'Authorized Official Telephone Number': 'AuthPhone',
            'Authorized Official Title or Position': 'position',
            'Provider Business Practice Location Address City Name': 'city',
            'NPI': 'NPI'
        }
        name_parts = ['Authorized Official First Name', 'Authorized Official Middle Name', 'Authorized Official Last Name']
        
        use_cols = list(column_mapping.keys()) + [c for c in name_parts]
        # Read with only needed columns if possible
        df = pd.read_csv(input_file, dtype=str, low_memory=False)
        
        update_progress(40, "Creating AuthOfficialName...")
        for part in name_parts: df[part] = df[part].fillna('')
        df['AuthOfficialName'] = df.apply(lambda r: ' '.join([r[p] for p in name_parts if r[p]]).strip(), axis=1)
        
        update_progress(70, "Finalizing columns...")
        existing_cols = [c for c in column_mapping.keys() if c in df.columns]
        final_df = df[existing_cols].copy()
        final_df.rename(columns=column_mapping, inplace=True)
        final_df['AuthOfficialName'] = df['AuthOfficialName']
        
        ordered_cols = ['UpdateDate', 'Legalbusinessname', 'State', 'OfficePhone', 'AuthOfficialName', 'AuthPhone', 'position', 'city', 'NPI']
        final_ordered = [c for c in ordered_cols if c in final_df.columns]
        final_df = final_df[final_ordered]
        
        output_name = 'uploadtosheet2026.csv'
        final_df.to_csv(output_name, index=False)
        
        progress_state['status'] = 'complete'
        progress_state['result_file'] = output_name
        update_progress(100, f"Saved {len(final_df):,} rows to {output_name}")
    except Exception as e:
        progress_state['status'] = 'error'
        update_progress(0, f"ERROR: {str(e)}")

# --- Flask Routes ---

@app.route('/')
def index():
    # List CSV files for selection in merger/formatter
    csv_files = [f for f in os.listdir('.') if f.lower().endswith('.csv')]
    return render_template('index.html', csv_files=csv_files)

@app.route('/api/progress')
def get_progress():
    return jsonify(progress_state)

@app.route('/api/filter', methods=['POST'])
def start_filter():
    data = request.json
    thread = threading.Thread(target=filter_task, args=(
        data.get('state'),
        data.get('update_start'),
        data.get('update_end'),
        data.get('enum_start'),
        data.get('enum_end'),
        data.get('taxonomies')
    ))
    thread.start()
    return jsonify({'status': 'started'})

@app.route('/api/merge', methods=['POST'])
def start_merge():
    data = request.json
    thread = threading.Thread(target=merge_task, args=(data.get('file1'), data.get('file2')))
    thread.start()
    return jsonify({'status': 'started'})

@app.route('/api/format', methods=['POST'])
def start_format():
    data = request.json
    thread = threading.Thread(target=format_task, args=(data.get('file'),))
    thread.start()
    return jsonify({'status': 'started'})

@app.route('/api/download/<filename>')
def download(filename):
    return send_file(os.path.join(BASE_DIR, filename), as_attachment=True)

if __name__ == '__main__':
    # Ensure templates folder exists
    os.makedirs(os.path.join(BASE_DIR, 'templates'), exist_ok=True)
    app.run(debug=True, port=5000)
