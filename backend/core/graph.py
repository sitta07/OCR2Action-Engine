from langgraph.graph import StateGraph, END
from core.state import GraphState
from core.nodes import extract_receipt, validate_receipt 

# 1. สร้าง Graph
workflow = StateGraph(GraphState)

# 2. เพิ่ม Node
workflow.add_node("extractor", extract_receipt)
workflow.add_node("validator", validate_receipt)

# 3. สร้างฟังก์ชันชี้ทางแยก (Router)
def route_validation(state: GraphState):
    if state.get("is_valid"):
        print("➡️ Routing: ข้อมูลถูกต้อง จบงาน! (เดี๋ยวไปต่อ RAG)")
        return "end"
    else:
        print("🔄 Routing: ข้อมูลผิดพลาด วนกลับไปสกัดใหม่!")
        return "extractor"

# 4. ลากเส้น Flow 
workflow.set_entry_point("extractor")
workflow.add_edge("extractor", "validator") # สกัดเสร็จ ต้องไปตรวจ QC เสมอ

# ถ้าตรวจ QC เสร็จ ให้ดูผลจาก route_validation ว่าจะจบ หรือจะวนลูป
workflow.add_conditional_edges(
    "validator",
    route_validation,
    {
        "end": END,         # ถ้า router return "end" → workflow จบ
        "extractor": "extractor"   # ถ้า return "extractor" → วนกลับไป extractor
    }
)


app_graph = workflow.compile()

print("\n--- 🗺️ LANGGRAPH WORKFLOW MAP ---")
print(app_graph.get_graph().draw_mermaid())
print("-----------------------------------\n")