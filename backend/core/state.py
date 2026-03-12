from typing import TypedDict, Optional, Dict, Any

class GraphState(TypedDict):
    raw_text: str                  # ข้อความดิบ (จำลองว่ามาจาก OCR)
    extracted_data: Optional[Dict[str, Any]] # ข้อมูล JSON ที่ AI สกัดได้
    is_valid: bool                 # ผ่านการ Validate Pydantic หรือยัง
    validation_errors: Optional[str] # เก็บ Error เอาไว้วนลูปให้ AI แก้ตัวเอง
    policy_decision: Optional[str]   # ผลตัดสินจาก RAG (Approve/Reject)

# หมายเหตุ: อันนี้คือโครงสร้างของกล่อง State ที่เราจะโยนให้ LangGraph (เหมือนกล่องที่พนักงานแต่ละคนจะหยิบไปใช้) --- IGNORE ---