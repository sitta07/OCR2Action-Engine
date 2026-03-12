import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from core.state import GraphState
from core.schema import ReceiptData

load_dotenv()

# ตั้งค่า Qwen API
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0  # ตั้งเป็น 0 เพื่อให้สกัดข้อมูลได้แม่นๆ ไม่หลอน
)

def extract_receipt(state: GraphState):
    print("--- 🔍 NODE: EXTRACTING DATA ---")
    raw_text = state["raw_text"]
    error_msg = state.get("validation_errors") # เช็กว่ารอบที่แล้วทำพังไหม
    
    # ถ้ามี Error จากรอบที่แล้ว ให้ส่งไปด่า LLM ด้วย
    prompt = f"""
        Extract information from this receipt text. 
        IMPORTANT RULES:
        1. If any field is missing, guess or put 'Unknown'.
        2. Correct any obvious spelling mistakes or OCR typos in Thai words (e.g., 'ไข่เจว' -> 'ไข่เจียว', 'ขาว' -> 'ข้าว'). Make the text grammatically correct.
        
        Text: {raw_text}
    """
    if error_msg:
         prompt += f"\n\n⚠️ PREVIOUS MISTAKE TO FIX: {error_msg}"

    structured_llm = llm.with_structured_output(ReceiptData)
    
    try:
        result = structured_llm.invoke(prompt)
        return {"extracted_data": result.model_dump(), "is_valid": False} # ตั้ง False ไว้ก่อน รอ Validator มาตรวจ
    except Exception as e:
        print(f"❌ Extraction Error: {e}")
        return {"is_valid": False, "validation_errors": str(e)}

# --- 🚀 โค้ดที่เพิ่มใหม่: ด่าน QC ---
def validate_receipt(state: GraphState):
    print("--- 🕵️‍♂️ NODE: VALIDATING DATA ---")
    data = state.get("extracted_data")
    
    if not data:
        return {"is_valid": False, "validation_errors": "No data extracted at all."}

    # สมมติ Logic ตรวจสอบง่ายๆ: ยอดเงินห้ามติดลบ หรือห้ามเป็น 0
    if data["total_amount"] <= 0:
        print("❌ Validation Failed: ยอดเงินผิดปกติ!")
        return {"is_valid": False, "validation_errors": "total_amount must be greater than 0"}

    # ถ้าผ่านเงื่อนไขทั้งหมด
    print("✅ Validation Passed: ข้อมูลผ่าน QC แล้ว!")
    return {"is_valid": True, "validation_errors": None}