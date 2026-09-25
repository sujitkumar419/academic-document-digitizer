import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')

def initialize_ingestion_folders():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

def ingest_scanned_document(uploaded_file_stream, filename):
    initialize_ingestion_folders()
    
    target_path = os.path.join(RAW_DIR, filename)
    with open(target_path, "wb") as f:
        f.write(uploaded_file_stream.getbuffer())
        
    return target_path

def cleanup_raw_storage():
    if os.path.exists(RAW_DIR):
        for file in os.listdir(RAW_DIR):
            file_path = os.path.join(RAW_DIR, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception:
                pass