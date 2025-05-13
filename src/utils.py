def log_message(message):
    print(f"[LOG] {message}")

def log_error(error_message):
    print(f"[ERROR] {error_message}")

def validate_task_data(task_data):
    if not isinstance(task_data, dict):
        log_error("Task data must be a dictionary.")
        return False
    if 'title' not in task_data or 'due_date' not in task_data:
        log_error("Task data must contain 'title' and 'due_date'.")
        return False
    return True