# Inception-Style AI Debate System using RAG

This project implements a dual-agent AI system where two language model agents engage in a structured debate using Retrieval-Augmented Generation (RAG). While the default example focuses on the *Inception* movie script, the system is designed to be **fully document-agnostic**, allowing users to define their own debate topics and knowledge sources.

---

## Motivation & Use Case

Large Language Models (LLMs) often rely solely on their internal knowledge, which can limit factual grounding and consistency. By integrating Retrieval-Augmented Generation (RAG), this project enriches agent responses with **user-provided documents**, enabling more accurate, contextual, and controllable debates.

Potential use cases include:
- Interactive AI storytelling
- Multi-agent reasoning simulations
- AI-based tutoring and argumentation systems
- Prompt engineering and RAG behavior analysis
- Prototyping conversational AI with evaluation logic

---

## System Architecture

The system follows a modular architecture separating retrieval, agent logic, evaluation, and user interaction.

```
+------------------+
| User Input |
| (Document + |
| Debate Roles) |
+--------+---------+
|
v
+-------------------------+
| Gradio Web UI |
| (gradio_main.py) |
+-----------+-------------+
|
v
+-------------------------+
| Debate Controller |
| (Conversation Loop) |
+-----------+-------------+
|
v
+-------------------------+
| Chat Agents (LLMs) |
| (chat_agent.py) |
+-----------+-------------+
|
v
+-------------------------+
| Retrieval-Augmented |
| Generation (RAG) |
| - Context Retrieval |
| - Prompt Injection |
+-----------+-------------+
|
v
+-------------------------+
| Evaluation / Judge |
| (judge.py) |
+-------------------------+
|
v
+-------------------------+
| Outputs & Logs |
+-------------------------+
```

---

## RAG Workflow & User Interaction

### Default Knowledge Source
By default, the system uses the *Inception* movie script as its knowledge base: 

data/inception.txt

This document is indexed and used by both agents during the debate.

---

### Custom Document Support

The system is **not limited to the default document**.

If a user wants the agents to debate a different topic, they can:

1. Prepare a `.txt` document containing the relevant content  
2. Upload the document via the **Gradio web interface**
3. Define what each LLM agent should argue or defend

Examples:
- Agent 1: *Defends a hypothesis*
- Agent 2: *Critiques or opposes the same hypothesis*

The uploaded document is then:
- Chunked using a sentence-based splitter
- Embedded with a HuggingFace embedding model
- Indexed into a vector store
- Queried dynamically during the debate using RAG

---

### Debate Flow (Step-by-Step)

1. **Document Selection**
   - Default: `data/inception.txt`
   - Or user-uploaded `.txt` file via UI

2. **Vector Index Creation**
   - Document is processed and stored as a vector index

3. **Persona & Role Definition**
   - User specifies the debate roles for each agent

4. **RAG-Enhanced Debate**
   - Each agent retrieves relevant context from the document
   - Responses are generated based on both persona instructions and retrieved content

5. **Evaluation**
   - A judge component evaluates responses qualitatively
   - Conversation continues with memory across turns

---

## Project Structure

````
inception_debate/
├── src/
│ ├── chat_agent.py # Agent prompt logic and response generation
│ ├── judge.py # Qualitative evaluation of debate responses
│ ├── utils.py # RAG, LLM, embedding, and retriever utilities
│ └── config.py # Environment variable loading (.env)
│
├── webapp/
│ └── gradio_main.py # Gradio-based web interface
│
├── data/
│ └── inception.txt # Default document used for RAG
│
├── .env # Environment variables (not committed)
├── .gitignore
├── requirements.txt
├── setup.sh # Automated project setup script
└── README.md
````

---

## Technologies Used

- Python
- LlamaIndex (Retrieval-Augmented Generation)
- Large Language Models (LLMs)
- Multi-Agent Systems
- HuggingFace Embeddings
- Gradio (Web UI)
- python-dotenv (Environment management)

---

## Project Setup

### 1. Clone the repository
```bash
git clone https://github.com/hasanerdin/inception_debate.git
cd inception_debate
```

### 2. Run setup script
```bash
chmod +x setup.sh
./setup.sh
```

### 3. Activate virtual environment
```bash
source venv/bin/activate
```

### 4. Run the application
```bash
python -m webapp.gradio_main
```

---

## Key Learnings
- RAG enables LLMs to ground arguments in user-provided knowledge
- Multi-agent debate setups encourage deeper reasoning than single-agent generation
- User-controlled personas significantly influence debate dynamics
- Modular system design improves extensibility and experimentation

---

## Limitations & Future Improvements
- Add quantitative evaluation metrics for debate quality
- Improve retrieval quality using advanced vector databases (e.g. FAISS, Chroma)
- Support multiple documents per debate
- Deploy as a containerized or cloud-based application

---

Author

Hasan Erdin

https://www.linkedin.com/hasanerdin/

https://www.github.com/hasanerdin/
