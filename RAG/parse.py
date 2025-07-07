import argparse
from llama_parse import LlamaParse
import os
import dotenv
from pathlib import Path
import re
dotenv.load_dotenv()

def extract_number(filename):
    # Extract the first group of digits from the filename
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else -1

def merge_txt_files(input_folder, output_file):
    """
    Merge all .txt files in input_folder into output_file.
    Files are merged in sorted order by filename.
    """
    input_folder = Path(input_folder)
    txt_files = sorted(
        input_folder.glob("*.txt"),
        key=lambda f: extract_number(f.name)
    )
    with open(output_file, "w", encoding="utf-8") as outfile:
        for txt_file in txt_files:
            with open(txt_file, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())
                outfile.write("\n")  # Optional: add newline between files
    print(f"Merged {len(txt_files)} files into {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Parse PDF and save each page as a text file.")
    parser.add_argument('--input', '-i', required=True, help='Path to the input PDF file')
    parser.add_argument('--output', '-o', required=True, help='Output folder to save parsed text files')
    parser.add_argument('--api_key', default=None, help='LlamaParse API key (optional, else from env)')
    parser.add_argument('--result_type', default='text', help='Result type for LlamaParse (default: text)')
    args = parser.parse_args()

    input_path = args.input
    output_folder = args.output
    api_key = args.api_key or os.getenv('LlamaParse')
    result_type = args.result_type

    # Ensure output directory exists
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    parser_llama = LlamaParse(
        api_key=api_key,
        result_type=result_type
    )

    extra_info = {"file_name": input_path}

    with open(input_path, "rb") as f:
        documents = parser_llama.load_data(f, extra_info=extra_info)

    # Save each document's text to separate txt files
    for i, doc in enumerate(documents):
        out_file = os.path.join(output_folder, f"page_{i}.txt")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(doc.text)
        print(f"Saved document {i} to {out_file}")

    print(f"Total documents saved: {len(documents)}")

if __name__ == "__main__":
    main()
