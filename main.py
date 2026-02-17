import os
import uvicorn
from pydantic import BaseModel
from google import genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
apiKey = os.getenv("GOOGLE_API_KEY")

if not apiKey:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

# Gemini client
client = genai.Client(api_key=apiKey)

app = FastAPI(
    title="Session Formatter API",
    description="Microservice to format student activity descriptions into Markdown.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextRequest(BaseModel):
    text: str

class DescriptionResponse(BaseModel):
    markdown: str

@app.get("/")
async def root():
    return {
        "Result": "Welcome To Chat MD API",
        "status": "active",
        "model" : "gemini-2.0-flash",
    }

@app.post('/format/description')
async def formatDescription(text : TextRequest):
    if len(text.text) < 5:
        raise HTTPException(status_code=400, detail="Input text is too short.")


    prompt = f"""
    You are an expert Technical Editor for a student activity website. Your goal is to convert session descriptions into engaging, structured Markdown.
    
    ### INPUT:
    You will receive text that might be a rough paragraph OR a list of notes (e.g., "Session Name:", "Topics:", "Resources:").
    {text}
    
    ### OUTPUT:
    Output ONLY the formatted Markdown code. Do not output code fences (```) or conversational text.
    
    ### FORMATTING RULES:
    1.  **Title:**
        -   Use the provided "Session Name" or "Title" as an H2 (## Title).
        -   If no title is provided, generate a catchy, professional H2 title based on the content.
    
    2.  **Summary:**
        -   Write a concise, high-energy opening paragraph (2-3 sentences) summarizing the session's value.
        -   Use the "We" voice (e.g., "In this session, we explored...").
    
    3.  **Key Topics:**
        -   Create a section header: `### 🚀 Key Topics`
        -   List topics using bullet points.
        -   **Crucial:** Do not just list the keyword. Add a short phrase explaining it.
        -   Format: `- **Topic Name**: Brief explanation of why it matters.`
    
    4.  **Resources (If present):**
        -   Create a section header: `### 📚 Resources`
        -   Detect any links provided in the text (often formatted as `[Name] [URL]` or just raw URLs).
        -   Convert them into proper clickable Markdown links: `-[Resource Name](URL)`.
    
    5.  **Styling:**
        -   **Bold** key technologies (e.g., **Python**, **Docker**, **React**).
        -   Fix all grammar, spelling, and capitalization errors.
    
    ### TONE:
    Professional, energetic, and encouraging. usage of emojis in headers is allowed to make it friendly.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
        )
        return DescriptionResponse(markdown=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate the response pls try again, {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
