from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
import os


app = FastAPI()

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # update if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = genai.Client(api_key="")
config = types.GenerateContentConfig();


@app.post("/extract")
async def extract(document: UploadFile = File(...)):
    content = await document.read()

    prompt = "Extract the claim, premises, and conclusion from this document."

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(
                data=content,
                mime_type=document.content_type,
            ),
            prompt
        ]
    )

    return {"arguments": response.text}
