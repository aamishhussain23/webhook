from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid

app = FastAPI()

# In-memory store for URLs (replace with a database in production)
stored_urls = set()

class CreateEndpointRequest(BaseModel):
    sheet: str

# CORS configuration to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/create-endpoint")
def create_endpoint(request: CreateEndpointRequest):
    while True:
        endpoint_id = uuid.uuid4()
        url = f"https://pingsheet.com/{endpoint_id}"
        if url not in stored_urls:
            stored_urls.add(url)
            break
    return {"url": url, "sheet": request.sheet}
