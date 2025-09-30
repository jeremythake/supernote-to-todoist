# supernote-to-todoist

## Overview
This project provides comprehensive synchronization between Supernote devices and Todoist, including task management and OCR capabilities for handwritten notes. It reads tasks from the Supernote calendar database and syncs them with Todoist, while also providing OCR functionality to convert handwritten notes to text using OpenAI's GPT-4 Vision API.

## Features
- **Task Synchronization**: Bidirectional sync between Supernote calendar tasks and Todoist
- **OCR Processing**: Convert handwritten Supernote files (.note) to searchable text using AI
- **Document Conversion**: Export notes to various formats (PNG, PDF, DOCX, TXT)
- **Automated Scheduling**: Run synchronization on a schedule using macOS LaunchAgents

## Project Structure
```
supernote-to-todoist/
├── src/
│   ├── main.py              # Main entry point for task synchronization
│   ├── supernote.py         # Core Supernote database functions
│   ├── todoist_api.py       # Todoist API integration
│   ├── ocr_sync.py          # OCR synchronization orchestrator
│   ├── supernote_to_text.py # Note-to-image conversion and OCR processing
│   ├── openaiconvert.py     # OpenAI GPT-4 Vision API integration
│   ├── convert-docx-txt.py  # DOCX to TXT conversion utility
│   ├── utils.py             # Utility functions for logging and error handling
│   ├── run_sync.sh          # Shell script for scheduled execution
│   ├── config.json          # Configuration settings (API keys, paths)
│   └── config.sample.json   # Sample configuration file
├── supernote/               # Directory for Supernote files (empty by default)
├── requirements.txt         # Python dependencies
├── com.supernote.sync.app.plist # macOS LaunchAgent configuration
└── README.md               # Project documentation
```

## Setup Instructions
1. Open a new terminal and clone the repository:
   ```
   mkdir Code
   cd Code
   git clone https://github.com/jeremythake/supernote-to-todoist
   cd supernote-to-todoist
   ```

2. Create the python virtual environment and check referenced correctly in `launch.json`. Change the paths to your environment.

```
cd ~/Code/supernote-to-todoist
/opt/homebrew/bin/python3.11 -m venv .venv
```

3. Install the required dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   brew install ghostscript
   brew install ocrmypdf
   pip install supernote-tool  # For .note file conversion
   ```

4. Configure your settings:
   ```bash
   cp src/config.sample.json src/config.json
   ```
   Open `config.json` and configure:
   1. **Todoist API Key**: Get your API token from [Todoist Settings](https://todoist.com/help/articles/find-your-api-token-Jpzx9IIlB) and add it to `todoist_api_key`
   2. **Supernote Database Path**: Find the calendar database at `~/Library/Containers/com.ratta.supernote/Data/Library/Application Support/com.ratta.supernote/[ID]/calendar_db.sqlite` and set the full path in `supernote_db_path`
   3. **OpenAI API Key** (for OCR features): Add your OpenAI API key to `openai_api_key` if you plan to use OCR functionality 


## Usage

### Task Synchronization
To run the main task synchronization between Supernote and Todoist:
```bash
~/Code/supernote-to-todoist/.venv/bin/python ~/Code/supernote-to-todoist/src/main.py
```

This will:
- Read tasks from the Supernote calendar database
- Check for existing tasks in Todoist
- Create new tasks in Todoist as needed
- Sync completion status back to Supernote

### OCR Processing
To convert handwritten Supernote files to text:
```bash
~/Code/supernote-to-todoist/.venv/bin/python ~/Code/supernote-to-todoist/src/ocr_sync.py
```

This will:
- Process .note files modified today
- Convert them to PNG images
- Use OpenAI GPT-4 Vision to extract handwritten text
- Save results as DOCX files

### Document Conversion
To convert DOCX files to plain text:
```bash
~/Code/supernote-to-todoist/.venv/bin/python ~/Code/supernote-to-todoist/src/convert-docx-txt.py
```

## Scheduled Execution

To run synchronization on a schedule, this project uses macOS LaunchAgents with a shell script.

1. Make the sync script executable:
   ```bash
   chmod +x ~/Code/supernote-to-todoist/src/run_sync.sh
   ```

2. **Important**: Add Python to **System Settings → Privacy & Security → Full Disk Access**. 
   - Navigate to your Python executable (follow the symlink in `.venv/bin/python`)
   - Path typically looks like: `/opt/homebrew/Cellar/python@3.11/3.11.12/Frameworks/Python.framework/Versions/3.11/bin/python3.11`
   - Use **⌘+Shift+G** to navigate to this path and add it to Full Disk Access

3. Copy the launch agent configuration:
   ```bash
   cp com.supernote.sync.app.plist ~/Library/LaunchAgents/
   ```

4. Load the scheduled job:
   ```bash
   launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.supernote.sync.app.plist
   ```

5. Verify it's running:
   ```bash
   launchctl list | grep supernote
   ```

6. Check the logs (wait 5 minutes after setup):
   ```bash
   cat /tmp/supernote-automator.log
   ```

## Dependencies

The project requires the following Python packages (see `requirements.txt`):
- `requests` - HTTP requests for Todoist API
- `pandas` - Data manipulation
- `supernotelib` - Supernote file handling
- `ocrmypdf` - PDF OCR processing
- `transformers`, `torch`, `torchvision` - Machine learning models for OCR
- `pillow` - Image processing
- `python-docx` - DOCX file handling
- `easyocr` - Additional OCR capabilities
- `openai` - OpenAI API integration

External dependencies:
- `ghostscript` - PostScript/PDF processing
- `ocrmypdf` - OCR for PDF files
- `supernote-tool` - CLI tool for .note file conversion

## Configuration

The `config.json` file should contain:
```json
{
  "todoist_api_key": "your_todoist_api_token",
  "supernote_db_path": "/path/to/calendar_db.sqlite",
  "openai_api_key": "your_openai_api_key"
}
```

## Troubleshooting

### Common Issues
1. **Permission Denied**: Ensure Python has Full Disk Access in macOS System Settings
2. **Database Not Found**: Verify the Supernote database path in `config.json`
3. **API Errors**: Check that your Todoist and OpenAI API keys are valid
4. **OCR Not Working**: Ensure `supernote-tool` is installed and accessible

### Log Files
- LaunchAgent logs: `/tmp/supernote-automator.log`
- Check system logs: `log show --predicate 'subsystem contains "com.supernote.sync"' --last 1h`

## Contributing
Feel free to submit issues or pull requests if you have suggestions or improvements for the project.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
