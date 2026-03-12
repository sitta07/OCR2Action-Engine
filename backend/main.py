from fastapi import FastAPI
from pydantic import BaseModel
from core.graph import app_graph 

app = FastAPI(title="OCR2Action Engine API", version="1.0.0")

class ReceiptRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"status": "Engine is running! 🚀"}

@app.post("/process-receipt")
def process_receipt(request: ReceiptRequest):
    # 1. เตรียมกล่อง State โยนให้ LangGraph
    initial_state = {"raw_text": request.text}
    
    # 2. กดปุ่มเดินเครื่อง! (invoke)
    print(f"📥 Received Text: {request.text}")
    result = app_graph.invoke(initial_state)
    
    # 3. ส่งผลลัพธ์กลับไปให้ User
    return {
        "status": "Success" if result.get("is_valid") else "Failed",
        "extracted_data": result.get("extracted_data"),
        "errors": result.get("validation_errors")
    }