from pydantic import BaseModel, Field

class ReceiptData(BaseModel):
    shop_name: str = Field(description="ชื่อร้านค้า")
    total_amount: float = Field(description="ยอดเงินรวมสุทธิ")
    date: str = Field(description="วันที่ในบิล (YYYY-MM-DD)")
    items: list[str] = Field(description="รายการสินค้าที่ซื้อทั้งหมด")