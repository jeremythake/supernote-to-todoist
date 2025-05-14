import re


def create_task(api_token, task_id, task_content, due_date=None, description=None):
    import requests

    # Updated endpoint for creating tasks
    url = "https://api.todoist.com/rest/v2/tasks"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    data = {
        "content":  "[id:" + str(task_id) + "] " + task_content
    }

    if due_date:
        data["due_date"] = due_date  # Use ISO 8601 format (e.g., "2025-05-15")

    data["description"] = description  # Add the task id and description

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 429:
            error_details = response.json()
            retry_after = error_details.get("error_extra", {}).get("retry_after", "unknown")
            print(f"Rate limit reached. Retry after {retry_after} seconds.")
            return False
    
    if response.status_code != 200:
        raise Exception(f"Failed to create task: {response.status_code} {response.text}")

    return response.json()

def get_todoist_tasks_completed(api_token):
    import requests
    import datetime

    url = "https://api.todoist.com/sync/v9/completed/get_all"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    params = {
        "limit": 100  # Number of completed tasks to fetch
    }

    response = requests.post(url, headers=headers, params=params)

    if response.status_code == 429:
            error_details = response.json()
            retry_after = error_details.get("error_extra", {}).get("retry_after", "unknown")
            print(f"Rate limit reached. Retry after {retry_after} seconds.")
            return False
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch tasks: {response.status_code} {response.text}")
    tasks = response.json().get("items", [])  # Get filtered tasks (already completed)

    return tasks

def get_existing_tasks(api_token):
    import requests

    url = "https://api.todoist.com/rest/v2/tasks"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 429:
        error_details = response.json()
        retry_after = error_details.get("error_extra", {}).get("retry_after", "unknown")
        print(f"Rate limit reached. Retry after {retry_after} seconds.")
        return False

    if response.status_code != 200:
        raise Exception(f"Failed to fetch tasks: {response.status_code} {response.text}")

    tasks = response.json()  # Extract tasks from the response
    return tasks

def check_existing_tasks(tasks, task_id):
        for task in tasks:
            match = re.search(r"\[id:(\d+)\]", task.get('content', ''))
            if match and int(match.group(1)) == int(task_id):
                return True
        return False