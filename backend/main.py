from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    text: str

@app.post("/analyze")
async def analyze_query(query: Query):
    prompt = f"""
    Analyze this customer support query and provide:
    - Category (billing/technical/account)
    - Priority (low/medium/high)
    - Solution
    - Estimated time in hours
    
    Query: {query.text}
    """
    
    response = ollama.chat(model='phi', messages=[
        {
            'role': 'user',
            'content': prompt
        }
    ])
    
    return {"response": response['message']['content']}

@app.get("/health")
def health_check():
    return {"status": "ok"}