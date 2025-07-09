# acuguru_agent

## Running the FastAPI app

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Query the RAG agent:
   Send a POST request to `http://localhost:8000/rag-query` with JSON body:
   ```json
   { "query": "your question here" }
   ```
   The response will include the agent's answer and reasoning.

## Running the Streamlit Chatbot

1. Make sure dependencies are installed (see above).

2. Start the Streamlit app:
   ```bash
   streamlit run streamlit/chatbot.py
   ```

3. Make sure the FastAPI backend is running (see above). Interact with the chatbot in your browser at the provided URL.

## Query Logging and Database Import

- All queries and responses are logged in `query_log.jsonl` (JSON Lines format) in the project root.
- Each log entry contains: timestamp, query, answer, and reasoning.

### Importing Logs into SQLite

1. Make sure you have Python's `sqlite3` and `json` modules (standard library).
2. To import logs into a local SQLite database, run:
   ```bash
   python app/log_to_db.py
   ```
   This will create (or update) `query_log.db` with a `query_logs` table containing all log entries.

### Using the Log for Fine-Tuning

- The `query_log.jsonl` file is easy to process for fine-tuning or analytics.
- Each line is a JSON object. You can convert it to your desired format (e.g., OpenAI, HuggingFace) using a simple Python script.

---

For any questions or to extend the logging/database workflow, see the code in `app/query_logger.py` and `app/log_to_db.py`.
