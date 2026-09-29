import os
import tempfile
import httpx
import assemblyai as aai
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Set your AssemblyAI API key in a .env file or environment variable
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
aai.settings.api_key = ASSEMBLYAI_API_KEY
# If you created a Voice Agent in your AssemblyAI dashboard, put its ID here
AGENT_ID = os.getenv("ASSEMBLYAI_AGENT_ID", "your_agent_id_here")

app = FastAPI(
    title="AeroRescue API",
    description="AI-powered voice-first disaster response using AssemblyAI",
    version="1.0.0"
)

# Enable CORS for the browser frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TriageResponse(BaseModel):
    transcript: str
    summary: str
    urgency_score: int
    disaster_type: str
    key_needs: list[str]
    location: str | None

@app.get("/")
def read_root():
    return {"message": "AeroRescue AssemblyAI API is running."}

@app.post("/voice-agent-token")
async def get_voice_agent_token():
    """
    Generates a temporary token to authenticate the browser frontend
    directly with the AssemblyAI Voice Agent API.
    """
    if not ASSEMBLYAI_API_KEY:
        raise HTTPException(status_code=500, detail="ASSEMBLYAI_API_KEY is not set.")
        
    # The Voice Agent API uses a temporary token for frontend WebSocket connections.
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.assemblyai.com/v1/beta/auth/temp-token",
            headers={
                "Authorization": ASSEMBLYAI_API_KEY,
                "Content-Type": "application/json"
            },
            json={"agent_id": AGENT_ID}
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Failed to generate token: {response.text}")
            
        return response.json()

@app.post("/analyze-distress-call", response_model=TriageResponse)
async def analyze_distress_call(file: UploadFile = File(...)):
    """
    Receives an audio distress call, transcribes it using AssemblyAI,
    and extracts key triage information using LeMUR.
    """
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="File must be an audio file.")

    # Save uploaded file to a temporary file
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            content = await file.read()
            temp_audio.write(content)
            temp_audio_path = temp_audio.name
            
        # Transcribe audio using AssemblyAI
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(temp_audio_path)
        
        if transcript.status == aai.TranscriptStatus.error:
            raise HTTPException(status_code=500, detail=f"Transcription failed: {transcript.error}")
            
        # Use LeMUR to extract structured data
        prompt = """
        You are an AI triage assistant for emergency disaster response.
        Analyze the caller's transcript and extract the following information:
        1. A brief summary of the situation.
        2. Urgency score from 1 to 10 (10 being most urgent).
        3. Disaster type (e.g., Earthquake, Flood, Cyclone, Wildfire, Other).
        4. Key needs (e.g., Medical, Evacuation, Shelter).
        5. Location if mentioned.
        """
        
        # LeMUR Task
        result = transcript.lemur.task(
            prompt,
            final_model=aai.LemurModel.claude3_5_sonnet
        )
        
        questions = [
            aai.LemurQuestion(question="What is a brief summary of the situation?", answer_format="short sentence"),
            aai.LemurQuestion(question="What is the urgency score on a scale of 1-10?", answer_format="number only"),
            aai.LemurQuestion(question="What is the disaster type? Choose from: Earthquake, Flood, Cyclone, Wildfire, Other.", answer_format="single word"),
            aai.LemurQuestion(question="What are the key needs?", answer_format="comma separated list"),
            aai.LemurQuestion(question="What is the location mentioned?", answer_format="short string or 'Unknown'")
        ]
        
        qa_result = transcript.lemur.question(questions)
        answers = {q.question: q.answer for q in qa_result.response}
        
        urgency = 5
        try:
            urgency = int(answers[questions[1].question].strip())
        except ValueError:
            pass
            
        needs = [need.strip() for need in answers[questions[3].question].split(",")]

        response_data = TriageResponse(
            transcript=transcript.text,
            summary=answers[questions[0].question],
            urgency_score=urgency,
            disaster_type=answers[questions[2].question],
            key_needs=needs,
            location=answers[questions[4].question] if answers[questions[4].question] != "Unknown" else None
        )
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp file
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
