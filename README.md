## System Architecture

The system is designed as a state-driven graph. Instead of a linear script, the agent has the "agency" to decide its own path based on the database's feedback.

1.  **Intent Classification**: A guardrail node that filters out non-SQL or off-topic queries.
2.  **Semantic Retrieval**: Queries a **Qdrant Vector Store** to inject relevant column metadata into the LLM context, preventing hallucinations.
3.  **The ReAct Loop**:
    * **Agent**: Generates SQL queries using openai/gpt-oss-20b (via Groq).
    * **Tool**: Executes queries against the SQLite database using SQLAlchemy.
    * **Feedback**: If a query fails, the agent receives the error and self-corrects in the next loop.
4.  **Streamlit UI**: A ChatGPT-style interface that displays the agent's thought process and status updates in real-time.


# Tech Stack
**Language** : Python 3.10+

**LLM Orchestration** : LangGraph & LangChain

**LLM** : Groq (openai/gpt-oss-20b)

**Vector DB** : Qdrant (In-memory)

**Database** : SQLite

**Embeddings** : HuggingFace (all-mpnet-base-v2)

# Table Details

**name**: The full name of the employee which is unique

**designation**: The job title or role

**department**: The department name (AI, HR, Sales)

**salary**: The numeric value representing annual pay

**id**: The unique primary key


### 1. Prerequisites
Ensure you have Python 3.10+ installed. You will also need a **Groq API Key**.

-- Configuration

Create a .env file in the root directory:

Code snippet: 
GROQ_API_KEY=your_groq_api_key_here

### 2. Installation
```bash
# Clone the repository
git clone "[git repo](https://github.com/Hrithik-coder/SQL_AGENT.git)"

cd agentic-sql-analyst

# Install dependencies
pip install -r requirements.txt

# run employee_table.py for the table creation
python employee_table.py

first add some employee data by querying the agent then perform the various actions

# run the streamlit application
streamlit run app.py
