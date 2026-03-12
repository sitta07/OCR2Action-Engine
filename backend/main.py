from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="OCR2Action Engine API", version="1.0.0")

class ReceiptRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"status": "Engine is running! 🚀", "message": "Ready to process documents."}

@app.post("/process-receipt")
def process_receipt(request: ReceiptRequest):
    # TODO: เดี๋ยวเราจะเอา LangGraph Workflow มาเสียบตรงนี้ในสเต็ปถัดไป
    return {
        "status": "Pending AI Processing",
        "input_text": request.text
    }
