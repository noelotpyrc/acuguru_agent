from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.rag_agent import react
from app.query_logger import log_query
import dspy
import dotenv
dotenv.load_dotenv()
import os

model_name = "openrouter/" + "openai/gpt-4o-mini"

lm = dspy.LM(model_name, api_key=os.getenv('OPENROUTER_API_KEY'), api_base=os.getenv('OPENROUTER_API_BASE'))
dspy.configure(lm=lm)

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/rag-query")
def rag_query(request: QueryRequest):
    try:
        result = react(query=request.query)
        # Log the query and response (now in JSONL format)
        log_query(request.query, result.answer, result.reasoning)
        return {
            "answer": result.answer,
            "reasoning": result.reasoning
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 