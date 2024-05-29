from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from datetime import datetime

app = FastAPI()

# In-memory store for URLs and hits (replace with a database in production)
stored_urls = set()
hits = []

class CreateEndpointRequest(BaseModel):
    sheet: str

class HitDetails(BaseModel):
    url: str
    method: str
    hostname: str
    user_agent: str
    date_time: str

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
        # url = f"http://127.0.0.1:8000/{endpoint_id}"
        if url not in stored_urls:
            stored_urls.add(url)
            break
    return {"url": url, "sheet": request.sheet}

@app.api_route("/{endpoint_id}", methods=["POST", "PUT", "GET", "PATCH", "DELETE"])
async def webhook(endpoint_id: str, request: Request):
    url = f"https://pingsheet.com/{endpoint_id}"
    # url = f"http://127.0.0.1:8000/{endpoint_id}"
    if url not in stored_urls:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    
    hit_details = HitDetails(
        url=url,
        method=request.method,
        hostname=request.client.host,
        user_agent=request.headers.get('user-agent', 'Unknown'),
        date_time=datetime.now().strftime("%d-%m-%Y %H:%M")
    )
    hits.append(hit_details.dict())
    return {"message": "Webhook received", "hit_details": hit_details.dict()}

@app.get("/hits")
def get_hits():
    return hits
