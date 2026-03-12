from langgraph.graph import StateGraph, END
from core.state import GraphState
from core.nodes import extract_receipt

# 1. สร้าง Graph 
workflow = StateGraph(GraphState)

# 2. เพิ่ม Node 
workflow.add_node("extractor", extract_receipt)

# 3. ลากเส้น Flow (จากจุดเริ่มต้น -> Extractor -> จบงาน)
workflow.set_entry_point("extractor")
workflow.add_edge("extractor", END)

# 4. Compile ระบบให้พร้อมใช้งาน
app_graph = workflow.compile()