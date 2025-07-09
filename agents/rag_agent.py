import dspy
from RAG.chroma import search_chroma
from RAG.embedder import ollama_embedder

def search(query, top_k=5):
    q_vec = ollama_embedder(query)
    res = search_chroma(q_vec[0])
    return res

instructions = "You are a holistic health expert. You are given a query and you need to answer it based on the information in the TCM database."
signature = dspy.Signature("query: str -> answer: str", instructions)
react = dspy.ReAct(signature, tools=[search], max_iters=20)

# example usage
# result = react(query="what is the sequence of the shang han lun levels?")
# print(result)
# result is a Prediction object with the following attributes:
# - answer: str
# - reasoning: str
# - trajectory: dict







