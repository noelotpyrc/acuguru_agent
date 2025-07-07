import argparse
import time
from embedder import load_corpus_from_file, ollama_embedder
from chroma import get_chroma_client, get_or_create_collection, add_embeddings


def main():
    parser = argparse.ArgumentParser(description="Chunk a text file and add embeddings to ChromaDB.")
    parser.add_argument('--input_folder', '-i', required=True, help='Folder containing the merged.txt file')
    parser.add_argument('--file_name', '-f', required=True, help='Name of the file (used for collection and metadata)')
    parser.add_argument('--collection_name', '-c', default=None, help='ChromaDB collection name (defaults to file_name)')
    parser.add_argument('--max_characters', type=int, default=6000, help='Max characters per chunk')
    parser.add_argument('--db_path', default='./chroma_store', help='ChromaDB storage path')
    args = parser.parse_args()

    input_file = f"{args.input_folder}/merged.txt"
    file_name = args.file_name
    collection_name = args.collection_name or file_name

    print(f"Loading and chunking {input_file} ...")
    corpus = load_corpus_from_file(input_file, max_characters=args.max_characters)
    print(f"Loaded {len(corpus)} chunks.")

    print(f"Connecting to ChromaDB at {args.db_path} ...")
    client = get_chroma_client(args.db_path)
    collection = get_or_create_collection(client, collection_name)

    print("Embedding and adding chunks to ChromaDB one by one ...")
    start_time = time.time()
    for idx, chunk in enumerate(corpus):
        chunk_start = time.time()
        embedding = ollama_embedder([chunk])[0]  # get embedding for this chunk
        add_embeddings(collection, [chunk], [embedding], file_name)
        elapsed = time.time() - start_time
        chunk_time = time.time() - chunk_start
        print(f"Processed chunk {idx+1}/{len(corpus)} (this chunk: {chunk_time:.2f}s, total: {elapsed:.2f}s)")

    print(f"Done. Added {len(corpus)} chunks to ChromaDB collection '{collection_name}'. Total time: {time.time() - start_time:.2f}s.")

if __name__ == "__main__":
    main() 