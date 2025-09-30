from pathlib import Path
import subprocess
from docx import Document
from openaiconvert import extract_handwritten_text_from_image

def note_to_png(openai_api_key, note_path: str, dpi: int = 600, model_name: str = 'microsoft/trocr-large-handwritten') -> str:
    print(f"Running OCR on {note_path} to text")

    note_path = Path(note_path).resolve()
    output_dir = Path("/Users/jeremythake/Desktop/supernote_ocr_output")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_base = output_dir / note_path.stem

    subprocess.run([
        "/Users/jeremythake/Code/supernote-to-todoist/.venv/bin/supernote-tool", "convert",
        "-t", "png",
        "-a",
        str(note_path),
        str(output_base)
    ], check=True)

    for f in output_base.parent.glob(f"{output_base.name}_*"):
                        if f.is_file() and f.suffix == "":
                            f.rename(f.with_suffix(".png"))

    page_text = []
    page_images = sorted(output_dir.glob(f"{note_path.stem}_*.png"))
    if not page_images:
        raise FileNotFoundError(f"No page images found for {note_path}")

    for img_path in page_images:
        #TODO only process the page if it has not been done before to save $$$
        text = extract_handwritten_text_from_image(openai_api_key, img_path)
        page_text.append(text)  

    return "\n\n".join(page_text) 


def save_text_to_docx(text: str, output_path: str | Path):
    print(f"Save docx to {str(output_path)}")
    doc = Document()
    for paragraph in text.split("\n"):
        doc.add_paragraph(paragraph.strip())
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))

