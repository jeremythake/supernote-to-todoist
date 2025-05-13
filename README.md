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

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure your settings:
   - Open `config.json` and add your Todoist API key and database connection settings.

## Usage
To run the synchronization script, execute the following command:
```
python src/main.py
```

This will read tasks from `supernote.db`, check for existing tasks in Todoist, and create any new tasks as necessary.

## Contributing
Feel free to submit issues or pull requests if you have suggestions or improvements for the project.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.