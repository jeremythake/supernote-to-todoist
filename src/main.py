import json
import re
import sqlite3
import datetime
import os
import sys
import base64
from todoist_api import create_task, check_existing_tasks, get_existing_tasks, get_todoist_tasks_completed
from supernote import update_supernote_task_status, get_supernote_tasks_needsAction, decode_metadata, convert_timestamp_to_date, get_supernote_tasks_all

os.chdir("/Users/jeremythake/Code/supernote-to-todoist")

from datetime import datetime
print(f"==== Supernote sync ran at {datetime.now().isoformat()} ====")

def load_config():
   base_dir = os.path.dirname(os.path.abspath(__file__))
   config_path = os.path.join(base_dir, 'config.json')
   with open(config_path) as config_file:
        return json.load(config_file)

def sync_tasks():
    # Column positions (based on the database structure)
    TASK_ID_POS = 0
    TASK_CONTENT_POS = 3
    DUE_DATE_POS = 10
    STATUS_POS = 8
    REMINDER_DATE_POS = 9
    METADATA_POS = 12  # Base64 encoded metadata

    supernote_tasks = get_supernote_tasks_needsAction(db_path)

    # Step 1: Sync completed tasks from Todoist to Supernote
    todoist_completed_tasks = get_todoist_tasks_completed(todoist_api_token)  # Fetch completed tasks from Todoist
    for todoist_task in todoist_completed_tasks:        
        match = re.search(r"\[id:(\d+)\]", todoist_task.get('content', ''))
        for task in supernote_tasks:
            if match and task[TASK_ID_POS] == int(match.group(1)):
                print("Supernote task update from todoist", task[TASK_ID_POS], task[TASK_CONTENT_POS])
                # Update the task status in Supernote
                update_supernote_task_status(db_path, task[TASK_ID_POS], "completed")

    # Step 2: Sync tasks from Supernote to Todoist
    supernote_tasks = get_supernote_tasks_needsAction(db_path)
    existing_tasks = get_existing_tasks(todoist_api_token)
    for task in supernote_tasks:
        # Get task description (content)
        content = task[TASK_CONTENT_POS] if task[TASK_CONTENT_POS] else "Untitled Task"
        task_id = task[TASK_ID_POS]
        # Extract metadata for description
        description = ""
        if len(task) > METADATA_POS and task[METADATA_POS]:
            file_path, page = decode_metadata(task[METADATA_POS])
            if file_path:
                # Extract just the filename from the path
                file_name = os.path.basename(file_path)
                description = f"Supernote Source: {file_name}, Page: {page}"
        
        # Get due date
        due_date = ""
        if task[DUE_DATE_POS]:
            due_date = convert_timestamp_to_date(task[DUE_DATE_POS])
        
        # Get reminder date if due date is empty
        if not due_date and task[REMINDER_DATE_POS]:    
            due_date = convert_timestamp_to_date(task[REMINDER_DATE_POS])
        
        # Write task to Todoist     
        if not check_existing_tasks(existing_tasks, task_id):
            print("Creating task in Todoist",task_id, content, due_date, description)
            create_task(todoist_api_token, task_id, content, due_date, description)


if __name__ == "__main__":

    config = load_config()
    db_path = config['supernote_db_path']
    todoist_api_token = config['todoist_api_key']
    
    sync_tasks()
