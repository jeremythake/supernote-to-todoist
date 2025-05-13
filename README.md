# supernote-todoist-sync

## Overview
This project synchronizes tasks from the Supernote cloud service to Todoist. It reads tasks from a local SQLite database (`supernote.db`) and creates them in Todoist if they do not already exist.

## Project Structure
```
supernote-todoist-sync
├── src
│   ├── main.py          # Entry point of the script
│   ├── db_reader.py     # Functions to read from the supernote.db
│   ├── todoist_api.py   # Functions to interact with the Todoist API
│   └── utils.py         # Utility functions for logging and error handling
├── requirements.txt      # Python dependencies
├── config.json           # Configuration settings (API keys, database settings)
└── README.md             # Project documentation
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/supernote-todoist-sync.git
   cd supernote-todoist-sync
   ```

2. Create the python virtual environment and check referenced correctly in `launch.json`. Change the paths to your environment.

```
cd /Users/jeremythake/Code/supernote-to-todoist
/opt/homebrew/bin/python3.11 -m venv .venv
```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure your settings:
   - Open `config.json` 
     1. **add Todoist API token** - Go to Todoist to get the key for the *todoist_api_key* setting. See more at [https://www.todoist.com/help/articles/find-your-api-token-Jpzx9IIlB]
     2. **add database connection settings** - Find the calendar file location at `~/Library/Containers/com.ratta.supernote/Data/Library/Application Support/com.ratta.supernote` and there is a ID number folder, go into that and find the `calendar_db.sqlite` file. Use that full path for the *supernote_db_path* setting. 


## Usage
To run the synchronization script, execute the following command. Change the paths to your environment.
```
/Users/jeremythake/Code/supernote-to-todoist/.venv/bin/python /Users/jeremythake/Code/supernote-to-todoist/src/main.py
```

This will read tasks from `supernote.db`, check for existing tasks in Todoist, and create any new tasks as necessary. It will also sync back any tasks you mark as complete into the Supernote database.

## Schedule usage

To run on the schedule. The best way on MacOS is to use Automator. 

1. Create a new **Application**.
2. Add a **Run Shell script** Action from the library on left hand side.
3. Replace the command to run with the following. Adjusting the paths to your virtual environment and python script.

```
/Users/jeremythake/Code/supernote-to-todoist/.venv/bin/python /Users/jeremythake/Code/supernote-to-todoist/src/main.py >> /tmp/supernote-automator.log 2>&1
```
4. Save the application.
5. Add **SupernoteSync.app** to **System Settings → Privacy & Security → Full Disk Access**
6. Copy the **com.supernote.sync.app.plist** file to **~/Library/LaunchAgents/**.
6.  Open **Terminal**
7. Run below command to add this as a scheduled job.

`launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.supernote.sync.app.plist`

7. check its running by reading the logs
`cat /tmp/supernote-automator.log`

## Contributing
Feel free to submit issues or pull requests if you have suggestions or improvements for the project.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.