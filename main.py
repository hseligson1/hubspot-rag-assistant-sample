from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
import openai
from pinecone import Pinecone

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="HubSpot RAG Assistant")

# Initialize OpenAI and Pinecone
openai.api_key = os.getenv("OPENAI_API_KEY")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("hubspot-llms")

# Request and Response schemas
class Question(BaseModel):
    question: str

class Answer(BaseModel):
    question: str
    answer: str
    sources: List[str]

@app.post("/ask", response_model=Answer)
def ask_question(payload: Question):
    user_question = payload.question

    # Step 1: Embed the user question
    try:
        embedding_response = openai.embeddings.create(
            input=user_question,
            model="text-embedding-3-small"
        )
        query_embedding = embedding_response.data[0].embedding
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding error: {e}")

    # Step 2: Search Pinecone
    try:
        results = index.query(
            vector=query_embedding,
            top_k=5,
            include_metadata=True
        )
        matches = results.get("matches", [])
        if not matches:
            raise HTTPException(status_code=404, detail="No relevant documents found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pinecone query error: {e}")

    # Step 3: Construct context and prompt
    context = "\n\n".join([m["metadata"]["text"] for m in matches])
    prompt = f"Use the following HubSpot documentation to answer the question.\n\n{context}\n\nQ: {user_question}\nA:"

    # Step 4: Get GPT-4 answer
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that only answers based on the HubSpot's Developer documentation."},
                {"role": "user", "content": prompt}
            ]
        )
        final_answer = response.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI completion error: {e}")

    return Answer(
        question=user_question,
        answer=final_answer,
        sources=[m["metadata"]["text"] for m in matches]
    )

@app.get("/")
def root():
    return {"message": "Welcome to the HubSpot RAG Assistant API"}
