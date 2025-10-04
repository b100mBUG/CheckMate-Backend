from pydantic import BaseModel
from pydantic import EmailStr
from datetime import date

class OrderIn(BaseModel):
    salesman_id : int
    order_name : str
    order_detail : str
    order_quantity : int
    
    customer_name : str
    customer_email : EmailStr
    customer_contact : str
    
    longitude : float
    latitude : float

    class Config:
        form_attributes = True

class OrderOut(BaseModel):
    order_id: int
    salesman_id : int
    order_name : str
    order_detail : str
    order_quantity : int
    
    customer_name : str
    customer_email : EmailStr
    customer_contact : str
    
    longitude : float
    latitude : float
    order_status : str
    date_added: date
    
    class Config:
        form_attributes = True

class OrderEdit(BaseModel):
    order_name : str
    order_detail : str
    order_quantity : int
    
    customer_name : str
    customer_email : EmailStr
    customer_contact : str

    class Config:
        form_attributes = True
    