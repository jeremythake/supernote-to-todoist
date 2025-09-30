#!/bin/zsh
export PATH="/opt/homebrew/bin:$PATH"
~/Code/supernote-to-todoist/.venv/bin/python ~/Code/supernote-to-todoist/src/main.py  >> /tmp/supernote-sync.log 2>&1
~/Code/supernote-to-todoist/.venv/bin/python ~/Code/supernote-to-todoist/src/ocr_sync.py  >> /tmp/supernote-sync.log 2>&1