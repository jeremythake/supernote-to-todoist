def create_task(api_token, task_content, due_date=None, description=None):
    import requests

    # Updated endpoint for creating tasks
    url = "https://api.todoist.com/rest/v2/tasks"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    data = {
        "content": task_content
    }

    if due_date:
        data["due_date"] = due_date  # Use ISO 8601 format (e.g., "2025-05-15")

    if description:
        data["description"] = description  # Add the task description

    response = requests.post(url, headers=headers, json=data)

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
    if response.status_code != 200:
        raise Exception(f"Failed to fetch tasks: {response.status_code} {response.text}")
    tasks = response.json().get("items", [])  # Get filtered tasks (already completed)

    return tasks

def check_existing_tasks(api_token, task_content):
    import requests

    url = "https://api.todoist.com/sync/v9/sync"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    data = {
        "sync_token": "*",  # Use "*" to fetch all tasks
        "resource_types": '["items"]'  # Specify that we want to fetch tasks
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch tasks: {response.status_code} {response.text}")

    tasks = response.json().get("items", [])  # Extract tasks from the response

    for task in tasks:
        if task['content'] == task_content:
            return True
    return False