from pydantic import BaseModel
from datetime import date

class ProductIn(BaseModel):
    company_id: int
    product_name: str
    product_category: str
    product_description: str
    product_price: float
    product_quantity: int
    
    class Config:
        form_attributes = True
   
class ProductEdit(BaseModel):
    product_name: str
    product_category: str
    product_description: str
    product_price: float
    product_quantity: int
    
    class Config:
        form_attributes = True


class ProductOut(BaseModel):
    company_id: int
    product_id: int
    product_name: str
    product_category: str
    product_description: str
    product_price: float
    product_quantity: int
    date_added: date
    
    class Config:
        form_attributes = True