import os
from pathlib import Path
from docx import Document
   
def docx_to_txt(docx_path, txt_path):
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

def convert_all_docx_to_txt(input_dir, output_dir):
    for docx_file in input_dir.rglob("*.docx"):
        txt_file = output_dir / (docx_file.stem + ".txt")
        output_dir.mkdir(parents=True, exist_ok=True)
        docx_to_txt(docx_file, txt_file)
        print(f"Converted: {docx_file} -> {txt_file}")

if __name__ == "__main__":
    input_dir = Path("/Users/jeremythake/Library/CloudStorage/OneDrive-AvePoint/Supernote")

    output_dir = Path("/Users/jeremythake/Desktop/txt-export")  # Update as needed
    convert_all_docx_to_txt(input_dir, output_dir)