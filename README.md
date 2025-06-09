# NeoReach - Executive Relationship Intelligence Platform

## 🚀 Overview

NeoReach automatically tracks executive role changes, updates organizational hierarchies in Neo4j, and initiates personalized outreach - with human approval at every critical step.

## ✨ Key Features

- **🔍 Change Detection**: Monitor LinkedIn/HRIS for executive movements
- **🕸️ Relationship Mapping**: Visualize power structures in Neo4j
- **✉️ Smart Outreach**: Generate context-aware emails/call scripts
- **👩💻 Human Oversight**: Streamlit-powered approval workflows

## 📂 Project Structure

```text
neoreach/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── app/
│   ├── main.py
│   ├── agents/
│   │   ├── change_detector.py
│   │   ├── graph_mapper.py
│   │   └── outreach_engine.py
│   ├── core/
│   │   ├── neo4j.py
│   │   └── llm/
│   │       ├── api.py
│   │       └── prompts.py
│   ├── data/
│   │   ├── executives.cypher
│   │   └── email_templates.json
│   └── ui/
│       ├── approval_ui.py
│       └── visualizer.py
└── README.md
```
🛠️ Installation
Prerequisites
Docker 20.10+

Python 3.9+

git clone https://github.com/yourusername/neoreach.git
cd neoreach

cp .env.example .env
# Edit .env with your credentials

docker-compose up -d

# .env
NEO4J_URL=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neoreach123
HF_API_KEY=your_huggingface_key

