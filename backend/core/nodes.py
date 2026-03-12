import os
from langchain_groq import ChatGroq
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
    
    #บังคับให้ LLM คืนค่าเป็นฟอร์แมต Pydantic 
    structured_llm = llm.with_structured_output(ReceiptData)
    
    try:
        # สั่งรันโมเดล
        result = structured_llm.invoke(f"Extract information from this receipt text. If any field is missing, guess or put 'Unknown'. Text: {raw_text}")
        
        # อัปเดต State ส่งต่อให้ Node ถัดไป
        return {"extracted_data": result.model_dump(), "is_valid": True, "validation_errors": None}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"is_valid": False, "validation_errors": str(e)}