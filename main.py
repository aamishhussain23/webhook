from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI()

# In-memory store for URLs (replace with a database in production)
stored_urls = set()

class CreateEndpointRequest(BaseModel):
    sheet: str

@app.post("/create-endpoint")
def create_endpoint(request: CreateEndpointRequest):
    while True:
        endpoint_id = uuid.uuid4()
        url = f"https://pingsheet.com/{endpoint_id}"
        if url not in stored_urls:
            stored_urls.add(url)
            break
    return {"url": url, "sheet": request.sheet}
