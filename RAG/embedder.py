import ollama
from pathlib import Path

def load_corpus_from_file(file_path, max_characters=6000):
    """
    Loads a single text file and splits it into chunks of up to max_characters.
    Returns a list of text chunks.
    """
    corpus = []
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        # Split text into chunks of max_characters
        for i in range(0, len(text), max_characters):
            corpus.append(text[i:i+max_characters])
    print(f"Loaded {len(corpus)} chunks from {file_path}.")
    return corpus

def ollama_embedder(text, model='qwen3:8b'):
    embed_result = ollama.embed(
        model=model,
        input=text,
    )
    return embed_result.embeddings