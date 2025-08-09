# Instalily Case Study

## Demo Video
https://www.loom.com/share/13120964c7534b63974e4571b0f493eb?sid=edf7104f-a3c7-49f9-9517-dbe08958a583

## 📌 Project Overview
This project is an **appliance parts customer support assistant** case study, simulating an intelligent customer service system that can instantly answer questions related to appliance parts. The data source is the **PartSelect dataset** (`partselect_parts.json`).  
The system can handle the following types of queries:
- Part lookup and function descriptions
- Step-by-step installation guidance
- Model compatibility checks
- Repair and troubleshooting advice
- General maintenance and usage tips

The backend is built with **FastAPI** and implements a custom **RAG (Retrieval-Augmented Generation) retrieval pipeline**, supporting multiple LLM providers (default: OpenAI, switchable to DeepSeek).

---

## 🎯 Key Features
1. **Rules Layer**  
   - Hardcoded answers for common questions (e.g., installation steps, compatibility checks, ice maker troubleshooting) to ensure 100% accurate responses.

2. **RAG Retrieval Layer**  
   - Uses OpenAI embeddings to vectorize part data and a pure Python cosine similarity search to return the top-matching part information.  
   - Strict prompt control: if retrieval results are insufficient, responds with "I'm not sure".

3. **Fallback LLM Layer**  
   - When both the Rules and RAG layers cannot answer, activates the LLM to provide general maintenance and troubleshooting suggestions.

4. **Multi-provider LLM API**  
   - Defaults to OpenAI, can switch to DeepSeek (requires setting `DEFAULT_PROVIDER` and API keys).  
   - Embeddings are always generated using OpenAI.

5. **Error Handling & Downgrade Mechanism**  
   - If DeepSeek has no credits or API key is missing, automatically falls back to OpenAI or returns a prompt message.

---

## 🏗 System Structure & File Purpose

```plaintext
instalily-case-study-cn/
├── backend/                     # Backend (FastAPI + RAG)
│   ├── agents/
│   │   ├── __init__.py          # Package initializer (can be empty)
│   │   └── partselect_agent.py  # Main agent logic: orchestrates Rules/RAG/LLM responses
│   ├── data/
│   │   └── partselect_parts.json# PartSelect dataset (knowledge base for RAG retrieval)
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── deepseek_api.py      # DeepSeek API wrapper (error handling, timeout, etc.)
│   │   ├── llm_api.py           # Provider router: chooses OpenAI/DeepSeek by DEFAULT_PROVIDER
│   │   └── openai_api.py        # OpenAI API wrapper (chat/completion unified interface)
│   ├── rag/
│   │   └── rag_index.py         # RAG retrieval: vectorization, cosine similarity, Top-K retrieval
│   ├── utils/
│   │   └── partselect_utils.py  # Field extraction/cleaning/formatting utilities for part data
│   ├── main.py                  # FastAPI entry point: /chat API, CORS, health checks
│   └── requirements.txt         # Backend Python dependencies (only keep this one)
├── frontend/                    # Frontend (React / CRA)
│   ├── node_modules/            # Installed NPM packages (do not version control)
│   ├── public/
│   │   ├── index.html           # CRA container HTML
│   │   └── manifest.json        # PWA/resource manifest
│   ├── src/
│   │   ├── api/
│   │   │   └── api.js           # API wrapper for communicating with backend /chat
│   │   ├── components/
│   │   │   ├── ChatWindow.css   # Chat window styles
│   │   │   └── ChatWindow.js    # Chat window UI (input box, message bubbles, loading states)
│   │   ├── App.css              # Global styles
│   │   ├── App.js               # App entry point, routing/state management
│   │   ├── index.js             # React DOM mounting point
│   │   ├── reportWebVitals.js   # Performance metrics (CRA default, optional)
│   │   └── setupTests.js        # Test initialization (CRA default, optional)
│   ├── package.json             # Frontend dependencies and scripts
│   └── package-lock.json        # Dependency lockfile (should be version controlled)
└── venv/                        # Python virtual environment (do not version control)
```

---

## ⚙️ Installation & Startup

### 1️⃣ Backend
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Set API keys
export OPENAI_API_KEY="your OpenAI API key"
export DEEPSEEK_API_KEY="your DeepSeek API key"  # optional

# Start backend server
cd backend
uvicorn main:app --reload
```
Backend runs by default on `http://127.0.0.1:8000`.

### 2️⃣ Frontend
```bash
cd frontend
npm install
npm start
```
Frontend runs by default on `http://localhost:3000`.

---

## 💡 Usage
The backend `/chat` API expects requests in the following format:
```json
{
  "message": "Is the water filter for model XYZ123 compatible?"
}
```
Processing steps:
1. **Rules Layer** → If matched, directly return predefined answer  
2. **RAG Layer** → Retrieve similar part data and generate an answer  
3. **Fallback LLM Layer** → If not matched, return "I'm not sure" or give general advice  

---

## 🧪 Test Cases
- **Installation Guidance**: "How to install the ice maker water inlet valve?" → Matches Rules Layer  
- **Compatibility Check**: "Is part #123 compatible with model ABC456?" → Matches RAG Layer  
- **Maintenance Advice**: "How often should I replace the fridge water filter?" → Matches Fallback LLM Layer  
- **Out-of-scope Question**: "Which laundry detergent brand is better?" → Returns "I'm not sure"  

---

## 📦 Dependency Management (`requirements.txt`)
- **Only keep `backend/requirements.txt`**, delete root-level `requirements.txt`.  
- To freeze dependencies in the future:
```bash
source venv/bin/activate
pip freeze > backend/requirements.txt
```
or:
```bash
pip install pipreqs
pipreqs backend --force --savepath backend/requirements.txt
```

---

## 🚫 Recommended `.gitignore`

```gitignore
# ---------- Python ----------
venv/
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.so
*.log
.mypy_cache/
.pytest_cache/
.cache/
dist/
build/
.eggs/
*.egg-info/
*.sqlite
*.db


!backend/data/partselect_parts.json

.env
.env.*
*.env

# ---------- Node / React (CRA) ----------
frontend/node_modules/
frontend/.env
frontend/.env.*
frontend/build/
frontend/dist/
frontend/.parcel-cache/
frontend/.next/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
*.tsbuildinfo

# ---------- OS / Editors ----------
.DS_Store
Thumbs.db
.idea/
.vscode/
*.swp

# ---------- Tests / Coverage ----------
coverage/
htmlcov/
*.cover
.tox/
```

---

## 📄 License
This project is for academic and case study purposes only. Dataset source: PartSelect.
