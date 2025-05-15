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
   brew install ghostscript
   brew install ocrmypdf
   ```

4. Configure your settings:
   ```bash
   cp src/config.example.json src/config.json
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

To run on the schedule. I learnt the hard way the best way is to have a **.sh script** and run it on a schedule using **launchctl**. 

1. Open the **run_sync.sh** file.
2. Replace the command to run with the following. Adjusting the paths to your virtual environment and python script.

```
/Users/jeremythake/Code/supernote-to-todoist/.venv/bin/python /Users/jeremythake/Code/supernote-to-todoist/src/main.py >> /tmp/supernote-automator.log 2>&1
```
3. Make the **run_sync.sh** executable in terminal:

```
chmod +x ~/Code/supernote-to-todoist/src/run_sync.sh
```   
5. Add **Python** to **System Settings → Privacy & Security → Full Disk Access**. You'll need to follow the alias in your **.env/bin/python** folder to get the path of the original. It will look something like this `/opt/homebrew/Cellar/python@3.11/3.11.12/Frameworks/Python.framework/Versions/3.11/bin` depending on the version. To show this folder its easiest to hit **command-shift-g** and paste in the path and select.
6. Copy the **com.supernote.sync.app.plist** file to **~/Library/LaunchAgents/**.
7. Adjust the path to the **main.py** file in the plist file.
8.  Open **Terminal**
9. Run below command to add this as a scheduled job.
```
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.supernote.sync.app.plist
```

10. Check its in the list:
```
launchctl list | grep supernote 
```

11. Give it 5 mins and check its running by reading the logs:
```
cat /tmp/supernote-automator.log
```

## Contributing
Feel free to submit issues or pull requests if you have suggestions or improvements for the project.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
