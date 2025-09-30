import json
import os
import shutil
import ocrmypdf
import subprocess
from datetime import datetime
from pathlib import Path
from supernote_to_text import note_to_png, save_text_to_docx

def load_config():
   base_dir = os.path.dirname(os.path.abspath(__file__))
   config_path = os.path.join(base_dir, 'config.json')
   with open(config_path) as config_file:
        return json.load(config_file)

def sync_ocr(openai_api_key):
    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            if file.lower().endswith(".note"):
                src = Path(root) / file
                if datetime.fromtimestamp(src.stat().st_mtime).date() == datetime.now().date(): # File was updated today #TODO: if i don't run daily this'll skip notes
                    rel_path = src.relative_to(INPUT_DIR).with_suffix(".pdf")
                    dest = OUTPUT_DIR / rel_path
                    rel_path_with_subdir = src.relative_to(INPUT_DIR.parent).with_suffix(".pdf")
                    docxdest = OUTPUT_DIR / rel_path_with_subdir.with_name(rel_path_with_subdir.stem + "ocr").with_suffix(".docx")
                    dest.parent.mkdir(parents=True, exist_ok=True)

                    #if file has been modified since last run, or if it doesn't exist
                    if not docxdest.exists() or os.path.getmtime(src) > os.path.getmtime(docxdest):
                        print(f"Processing file: {file}")
                        # create PNG of notes
                        text = note_to_png(openai_api_key, src, dpi=600)
                        # write docx file
                        save_text_to_docx(text, docxdest)

                    # TODO: it tries to write to file that exists already . i modified the note after it had run this once!
                    # PermissionError: [Errno 1] Operation not permitted: '/Users/jeremythake/Library/CloudStorage/OneDrive-AvePoint/Supernote/Note/bill d/20250602_103251 bill docr.docx'


if __name__ == "__main__":
    print(f"==== Supernote OCR to OneDrive ran at {datetime.now().isoformat()} ====")
    config = load_config()
    openai_api_key = config['openai_api_key']
    INPUT_DIR = Path(config['INPUT_DIR'])
    OUTPUT_DIR = Path(config['OUTPUT_DIR'])

    sync_ocr(openai_api_key)

    print("Finished OCR conversion at {datetime.now().isoformat()} ====")