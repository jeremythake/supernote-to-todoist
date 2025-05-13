import json
import sqlite3
import datetime
import os
import sys
import base64

def convert_timestamp_to_date(timestamp_ms):
    """Convert Unix timestamp (milliseconds) to an ISO 8601 date string."""
    if not timestamp_ms:
        return ""
    
    # Convert milliseconds to seconds
    timestamp_sec = timestamp_ms / 1000
    
    # Convert to datetime
    task_date = datetime.datetime.fromtimestamp(timestamp_sec)
    
    # Format as ISO 8601 (e.g., "2025-05-15")
    return task_date.strftime("%Y-%m-%d")

def decode_metadata(metadata_base64):
    """Decode Base64 encoded metadata to extract file path and page."""
    if not metadata_base64:
        return "", ""
    
    try:
        # Decode Base64 to bytes, then convert to string
        metadata_json = base64.b64decode(metadata_base64).decode('utf-8')
        
        # Parse JSON
        metadata = json.loads(metadata_json)
        
        # Extract file path and page
        file_path = metadata.get('filePath', '')
        page = metadata.get('page', '')
        
        return file_path, page
    except Exception as e:
        print(f"Warning: Could not decode metadata: {e}")
        return "", ""
    
def get_supernote_tasks_needsAction(db_path):
    conn = sqlite3.connect(db_path, uri=True)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM task WHERE status = 'needsAction'")  
    tasks = cursor.fetchall()
    conn.close()
    return tasks  # Return all rows, not just the first column


def get_supernote_tasks_all(db_path):
    conn = sqlite3.connect(db_path, uri=True)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM task")  
    tasks = cursor.fetchall()
    conn.close()
    return tasks  # Return all rows, not just the first column


def update_supernote_task_status(db_path, task_id, new_status):
    conn = sqlite3.connect(db_path, uri=True)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE task SET status = ? WHERE id = ?",
        (new_status, task_id)
    )
    conn.commit()
    conn.close()