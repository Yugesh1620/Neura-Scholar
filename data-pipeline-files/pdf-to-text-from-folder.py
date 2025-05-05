import os
import fitz  # PyMuPDF
from concurrent.futures import ProcessPoolExecutor, as_completed

def process_pdf(args):
    """
    Worker function for processing a single PDF.
    args: tuple(pdf_path, output_dir)
    Returns status message.
    """
    pdf_path, output_dir = args
    filename = os.path.basename(pdf_path)
    txt_filename = os.path.splitext(filename)[0] + '.txt'
    txt_path = os.path.join(output_dir, txt_filename)
    try:
        doc = fitz.open(pdf_path)
        text = "\n\n".join(page.get_text() for page in doc)
        doc.close()
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return f"Converted {filename} -> {txt_filename}"
    except Exception as e:
        return f"Failed {filename}: {e}"

def convert_pdfs_to_text(input_dir: str, output_dir: str, workers: int) -> None:
    """
    Extract text from all PDFs in input_dir using multiple processes,
    saving .txt files to output_dir.
    """
    os.makedirs(output_dir, exist_ok=True)
    # Build list of tasks
    pdfs = [
        os.path.join(input_dir, fn)
        for fn in os.listdir(input_dir)
        if fn.lower().endswith('.pdf')
    ]
    print(f"Starting conversion with {workers} processes...")
    # ProcessPool for CPU-bound tasks
    with ProcessPoolExecutor(max_workers=workers) as executor:
        future_to_pdf = executor.map(process_pdf, ((pdf, output_dir) for pdf in pdfs))
        for result in future_to_pdf:
            print(result)

def main():
    import sys
    if len(sys.argv) not in (3, 4):
        print(f"Usage: {sys.argv[0]} <input_folder> <output_folder> [num_processes]")
        sys.exit(1)
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    if len(sys.argv) == 4:
        try:
            workers = int(sys.argv[3])
        except ValueError:
            print("Number of processes must be an integer.")
            sys.exit(1)
    else:
        workers = os.cpu_count() or 4
    convert_pdfs_to_text(input_folder, output_folder, workers)

if __name__ == '__main__':
    main()

