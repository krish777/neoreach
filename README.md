# NeoReach - Executive Relationship Intelligence Platform

## 🚀 Overview

NeoReach now leverages CrewAI for intelligent agent orchestration while maintaining human-in-the-loop approval workflows. The platform automatically tracks executive movements, maps organizational hierarchies, and initiates context-aware outreach.

## ✨ Key Features

- **🤖 CrewAI Agent Orchestration**:

  - Role-based specialized agents working in teams
  - Dynamic task delegation and collaboration
  - Built-in memory and context sharing

- **🔄 Human Workflow Integration**:

  - Approval gates at critical decision points
  - Streamlit-powered review interfaces
  - Audit trails for all automated actions
  - Human Approval Workflow in CrewAI

- **🔍 Enhanced Change Detection**:
  - Change Detection\*\*: Monitor LinkedIn/HRIS for executive movements
  - Multi-source monitoring (LinkedIn, news, SEC filings)
  - AI-powered relevance filtering
  - **✉️ Smart Outreach**: Generate context-aware emails/call scripts
  - Confidence scoring for detected changes

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
NEO4J_PASSWORD=
HF_API_KEY=your_huggingface_key

Getting Started 🚀
Prerequisites
Docker 24.0+

Python 3.10+

Neo4j 5.11+

CrewAI 0.28+

Key Components 🔍
Module Technology Stack Leadership Value
Change Detection CrewAI + LangChain Real-time market intelligence
Relationship Mapping Neo4j + Graph Algorithms Strategic org insights
Approval Workflows Streamlit + FastAPI Compliance assurance
