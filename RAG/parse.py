import argparse
from llama_parse import LlamaParse
import os
import dotenv
from pathlib import Path

dotenv.load_dotenv()

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
