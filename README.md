# Visora — EDGE AR Industrial Knowledge Platform

Visora is a secure, edge-deployed AR (Augmented Reality) Knowledge Platform built for industrial and field service environments. It gives workers a hands-free, voice-activated AI assistant through AR glasses that sees what they see and answers questions in real time — drawing from official machine manuals and expert-recorded repair sessions. All AI processing runs locally using **Ollama**, with no cloud dependency.

---

## The Problem

Critical operational knowledge lives in the heads of experienced technicians. When they retire or leave, that knowledge disappears. New workers are left with outdated paper manuals, no real-time guidance, and no way to get help without stopping work and taking their hands off the machine. This leads to costly downtime, safety incidents, and slow onboarding.

---

## The Solution

Visora solves this with two core capabilities:

**1. Real-Time AR Assistance**
Workers wear AR glasses connected to a local edge server. They hold a button, ask a question out loud, and the AI sees what they see via the camera, searches the knowledge base, and speaks the answer back — hands-free.

**2. Automatic Knowledge Capture**
When an expert performs a repair, they record the session through the AR interface. The AI automatically analyzes the transcript, extracts the steps, tools, and safety notes, and stores it as a searchable entry in the knowledge base — permanently preserving institutional memory.

---

## Features

- **AR Simulator** — live camera feed simulating the AR glasses view, with push-to-talk voice commands
- **Vision-Aware AI** — captures frames from the camera feed and sends them to the AI for visual context
- **RAG Pipeline** — retrieves relevant chunks from ingested PDF manuals using ChromaDB + HuggingFace embeddings
- **Expert Session Recording** — saves repair transcripts with auto-extracted titles, summaries, and tool lists
- **Knowledge Base Chat** — web interface for querying both manuals and past expert sessions
- **Expert Summaries View** — browse all recorded sessions with thumbnails and extracted metadata
- **Fully Offline** — runs entirely on a local edge server, no internet required

---

## Tech Stack

### Backend
| Component | Technology |
|---|---|
| API Framework | FastAPI (Python) |
| AI Runner | Ollama (local, offline) |
| Vision + Chat Model | Llama 3.2 Vision via Ollama |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Vector Database | ChromaDB |
| Relational Database | SQLite |
| Speech-to-Text | Browser Web Speech API |

### Frontend
| Component | Technology |
|---|---|
| Framework | Vue 3 |
| Build Tool | Vite |
| Styling | Tailwind CSS |
| Routing | Vue Router |

---

## Project Structure

```
.
├── backend/
│   ├── main.py           # FastAPI app — chat, vision, upload, and video endpoints
│   ├── ingest.py         # PDF ingestion script — chunks and loads manuals into ChromaDB
│   ├── database.py       # SQLite schema initialization
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   │   ├── Simulator.vue        # AR glasses simulator — camera + voice interface
│   │   │   └── KnowledgeViewer.vue  # Knowledge base chat + expert summaries
│   │   ├── App.vue
│   │   └── main.js
│   └── package.json
├── tests/
│   ├── backend/
│   ├── edge/
│   └── e2e/
└── ar-glasses-app/       # AR glasses companion app
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- [Ollama](https://ollama.com) installed and running locally

### 1. Pull the required Ollama model
```bash
ollama pull llama3.2-vision
```

### 2. Set up the backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 3. Ingest your PDF manuals
Place your machine manual PDFs in the root directory, then run:
```bash
python ingest.py
```
This chunks the PDFs and loads them into the local ChromaDB vector database.

### 4. Start the backend
```bash
uvicorn main:app --reload --port 8000
```

### 5. Set up and start the frontend
```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

---

## How to Use

### AR Simulator (Worker Mode)
1. Navigate to the **AR Simulator** tab
2. Click **Start Camera Feed** to activate the live camera
3. Hold the microphone button and ask a question (e.g. *"What is this component?"* or *"How do I safely remove the battery?"*)
4. Release the button — the AI analyzes the camera frame and your question, then speaks the answer back

### Expert Recording (Expert Mode)
1. Start the camera and ask a question while performing a repair
2. After the AI responds, click **Save as Expert Video**
3. The AI extracts a title, summary, and tools list from the session transcript
4. The session is now searchable in the Knowledge Base

### Knowledge Base
1. Navigate to the **Knowledge Base** tab
2. Use the **Knowledge Chat** to ask questions — the RAG pipeline searches both manuals and expert sessions
3. Browse **Expert Summaries** to view all recorded sessions

---

## Architecture Overview

```
AR Glasses / Browser
       |
       | (audio + camera frames)
       v
  FastAPI Backend
       |
   ┌───┴───┐
   |       |
   v       v
ChromaDB  Ollama (local)
(Vector   (llama3.2-vision)
 Search)
   |       |
   └───┬───┘
       |
   RAG Answer
       |
       v
  Spoken Response (Web Speech API TTS)
```

---

## Environment Variables

Create a `.env` file in the `backend/` directory:

```
OLLAMA_BASE_URL=http://localhost:11434
```

---

## Team

Built for the EDGE Hackathon.
