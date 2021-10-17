# QL-BOT

Natural-language interface for querying and updating a sample employee SQLite database, powered by a LangGraph agent and Groq.

## Overview

QL-BOT (Agentic SQL Analyst) combines intent classification, vector-based schema retrieval, and a ReAct-style SQL tool loop so users can ask questions in plain English instead of writing SQL by hand. A Streamlit chat UI streams agent status while the graph classifies the request, retrieves column context from an in-memory Qdrant store, generates SQL via Groq, and executes allowed statements against SQLite.

## Features

- Chat UI with session history and a clear-history control
- Guardrail node that rejects off-topic prompts before SQL runs
- Semantic schema retrieval (HuggingFace embeddings + Qdrant) to ground the LLM
- LangGraph workflow: classify → retrieve → agent ↔ tools
- SQL execution limited to `SELECT`, `INSERT`, `UPDATE`, and `DELETE` (blocks DDL)
- Sample `employees` table seeded for local demos

## Tech stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| UI | Streamlit |
| Orchestration | LangGraph, LangChain |
| LLM | Groq (`openai/gpt-oss-20b`) |
| Vector store | Qdrant (in-memory) |
| Embeddings | `sentence-transformers/all-mpnet-base-v2` |
| Database | SQLite via SQLAlchemy |

## Prerequisites

- Python 3.10 or newer
- A [Groq](https://console.groq.com/) API key

## Getting started

```bash
git clone https://github.com/vonmiller1/QL-BOT.git
cd QL-BOT
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Copy the environment template and set your key (names only—never commit real secrets):

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux
```

Required variable:

- `GROQ_API_KEY` — Groq API key used by `ChatGroq`

Initialize the SQLite database and seed sample data:

```bash
python employee_table.py
```

## Running locally

```bash
streamlit run app.py
```

Streamlit serves the app at [http://localhost:8501](http://localhost:8501) by default.

Example prompts:

- "List all employees in the AI department."
- "Give hrithik a 10% raise and show the updated salary."

## Testing

This repository does not ship automated tests. To verify manually, start the app, run a few SELECT queries, then try an off-topic question to confirm the classifier blocks it.

## Project structure

```
QL-BOT/
├── app.py              # Streamlit entrypoint
├── agent_code.py       # LangGraph graph, tools, and nodes
├── employee_table.py   # SQLite engine and schema seed script
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── README.md
```

Runtime artifacts (not committed): `employee_db.sqlite`, local `.env`.

## Configuration

| Variable | Purpose |
|----------|---------|
| `GROQ_API_KEY` | Authenticates Groq LLM calls |

Qdrant runs in-process (`:memory:`); no separate vector DB service is required for local use.

## Deployment

No Dockerfile or CI workflow is included. For production you would externalize secrets, use a persistent Qdrant instance, and harden SQL policies beyond the demo guardrails.

## Contributing

1. Fork the repository and create a feature branch.
2. Keep commits focused (one logical change per commit when possible).
3. Open a pull request with a short description of behavior and setup impact.

## License

No `LICENSE` file is present in this repository; add one if you plan to distribute or accept contributions under explicit terms.
