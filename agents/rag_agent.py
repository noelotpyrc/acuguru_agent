import dspy
from tools.chroma_tool import search_chroma

instructions = "Placeholder"
signature = dspy.Signature("query: str -> answer: str", instructions)
react = dspy.ReAct(signature, tools=[search_chroma], max_iters=20)








