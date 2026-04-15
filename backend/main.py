from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sqlite3
import json
from typing import List, Optional
import speech_recognition as sr
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
import tempfile
import asyncio
import time

app = FastAPI(title="EDGE Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str
    role: str
    images: List[str] = []

class VideoUploadRequest(BaseModel):
    transcript: str
    role: str
    thumbnail: Optional[str] = None

# Initialize AI components globally
DB_DIR = "./chroma_db"
retriever = None
llm = None

def init_db():
    print("[DB] Initializing SQLite database...")
    conn = sqlite3.connect("edge_platform.db")
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS videos (id INTEGER PRIMARY KEY, transcript TEXT, role TEXT, thumbnail TEXT)")
        cursor.execute("ALTER TABLE videos ADD COLUMN thumbnail TEXT")
    except sqlite3.OperationalError:
        pass # Column already exists
    conn.commit()
    conn.close()
    print("[DB] Database ready.")

def _load_ai_components():
    """Blocking initialization — must be called from a thread, not the event loop."""
    global retriever, llm
    start_total = time.time()
    try:
        from langchain_community.vectorstores import Chroma
        from langchain_community.embeddings import HuggingFaceEmbeddings

        print("[AI] Loading Embedding Model (HuggingFace)...")
        start = time.time()
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        print(f"[AI] Embeddings loaded in {time.time()-start:.1f}s")

        print("[AI] Connecting to Vector Store (Chroma)...")
        start = time.time()
        vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        print(f"[AI] Vector Store ready in {time.time()-start:.1f}s")

        print("[AI] Initializing Groq API...")
        start = time.time()
        llm = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        print(f"[AI] Groq initialized in {time.time()-start:.1f}s")

        print(f"[AI] FULL PIPELINE READY in {time.time()-start_total:.1f}s!")
    except Exception as e:
        print(f"[AI] CRITICAL ERROR during AI initialization: {e}")

async def init_ai_async():
    # Run the blocking work in a thread so the event loop stays responsive
    # (allows CTRL+C and health-check requests to work while models load)
    await asyncio.to_thread(_load_ai_components)

@app.on_event("startup")
async def startup_event():
    init_db()
    # Start AI loading in the background so server can respond immediately
    asyncio.create_task(init_ai_async())

@app.get("/")
def read_root():
    return {"status": "ok", "ai_ready": llm is not None}

@app.post("/chat")
def chat_with_rag(request: ChatRequest):
    if llm is None or retriever is None:
        return {"answer": "System Warning: The AI Backend is currently in Mock mode because Gemini or the Vector Database failed to initialize. Did you run the ingest script and set GEMINI_API_KEY?"}
        
    print(f"[{request.role} Query]: {request.query}")
    
    try:
        # Custom RAG implementation bypasses versioning issues
        docs = retriever.invoke(request.query)
        context = "\n".join([doc.page_content for doc in docs])
        
        prompt = f"""You are a hands-free voice assistant for automotive and industrial technicians.
Use the following reference manual context to help answer the question:
{context}

User question: {request.query}

Instructions:
- Give a concise, spoken-friendly answer (1-3 sentences max).
- If the user asks where something is located and you can see it in the image, describe its position naturally using simple terms like: top-left, top-right, center, bottom-left, bottom-right, upper area, lower area, left side, right side.
- Example: "The oil filler cap is in the top-right area of the engine bay, next to the intake manifold."
- Do NOT output any coordinates, numbers, or special tags.
- Speak as if you are guiding someone who cannot look at the screen.
"""
        
        if not request.images:
            messages = [{"role": "user", "content": prompt}]
        else:
            content = [{"type": "text", "text": prompt}]
            for img_b64 in request.images:
                if "," in img_b64:
                    img_b64 = img_b64.split(",", 1)[1]
                content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}})
            messages = [{"role": "user", "content": content}]

        model = "meta-llama/llama-4-scout-17b-16e-instruct" if request.images else "llama-3.3-70b-versatile"
        response = llm.chat.completions.create(model=model, messages=messages)
        answer = response.choices[0].message.content

        print(f"[RAW MODEL ANSWER]: {answer}")
        return {"answer": answer}
    except Exception as e:
        print(f"Error during RAG: {e}")
        return {"answer": f"Error calling Gemini API. Please check that GEMINI_API_KEY is set correctly. Details: {str(e)}"}

@app.post("/ask-audio")
async def ask_audio(audio: UploadFile = File(...), image: Optional[str] = Form(None), role: str = Form("worker")):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(await audio.read())
            temp_path = temp_audio.name
            
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_path) as source:
            audio_data = recognizer.record(source)
            try:
                query = recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                os.remove(temp_path)
                return {"answer": "I couldn't hear that clearly, please repeat.", "transcribed": ""}
            except sr.RequestError:
                os.remove(temp_path)
                return {"answer": "Speech recognition service is unreachable.", "transcribed": ""}
        
        os.remove(temp_path)
        
        images_list = [image] if image else []
        chat_req = ChatRequest(query=query, role=role, images=images_list)
        return {"transcribed": query, **chat_with_rag(chat_req)}
        
    except Exception as e:
        return {"answer": f"Audio processing error: {e}", "transcribed": ""}

@app.post("/upload-video")
def upload_video(request: VideoUploadRequest):
    if llm is None:
        raise HTTPException(status_code=500, detail="AI Offline")
        
    prompt = f"""You are an automotive expert. Analyze the following repair transcript and extract a clear JSON with 3 keys:
- "title": A short 3-5 word title for the repair.
- "summary": A brief 1-2 sentence description of what is being done.
- "tools": Python list of short strings containing any tools or equipment mentioned. If none, return empty list.

Transcript: "{request.transcript}"

Respond ONLY with the raw JSON object, no markdown blocks. Do not add explanations.
"""
    try:
        response_text = llm.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        data = json.loads(response_text)
        
        title = data.get("title", "Expert Repair Session")
        summary = data.get("summary", "No summary provided.")
        tools = json.dumps(data.get("tools", []))
        
        conn = sqlite3.connect("edge_platform.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO videos (title, uploader_role, summary, extracted_tools, filepath, thumbnail)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, request.role, summary, tools, "internal_video.mp4", request.thumbnail))
        conn.commit()
        conn.close()
        
        return {"status": "success", "message": "Video indexed successfully!"}
    except Exception as e:
        print(f"Extraction Error: {e}")
        # Fallback dump
        conn = sqlite3.connect("edge_platform.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO videos (title, uploader_role, summary, extracted_tools, filepath, thumbnail)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ("Manual Repair Session", request.role, request.transcript[:100]+"...", "[]", "internal_video.mp4", request.thumbnail))
        conn.commit()
        conn.close()
        return {"status": "fallback", "message": "Saved string without AI extraction.", "error": str(e)}

@app.get("/videos")
def get_videos():
    try:
        conn = sqlite3.connect("edge_platform.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM videos ORDER BY id DESC")
        rows = cursor.fetchall()
        
        result = []
        for r in rows:
            tools_list = []
            if r['extracted_tools']:
                try:
                    tools_list = json.loads(r['extracted_tools'])
                except:
                    tools_list = [r['extracted_tools']]
            
            thumbnail_dat = None
            if 'thumbnail' in r.keys() and r['thumbnail']:
                thumbnail_dat = r['thumbnail']
                
            result.append({
                "id": r['id'],
                "title": r['title'],
                "role": r['uploader_role'],
                "summary": r['summary'],
                "tools": tools_list,
                "thumbnail": thumbnail_dat
            })
            
        conn.close()
        return {"videos": result}
    except Exception as e:
        return {"videos": [], "error": str(e)}
