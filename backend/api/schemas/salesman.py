from pydantic import BaseModel
from pydantic import EmailStr

class SalesmanIn(BaseModel):
    company_id : int
    salesman_name: str
    salesman_email: EmailStr
    salesman_contact : str
    salesman_password : str
    
    class Config:
        form_attributes = True

class SalesmanOut(BaseModel):
    salesman_id: int
    company_id : int
    salesman_name: str
    salesman_email: EmailStr
    salesman_contact : str
    
    class Config:
        form_attributes = True

class SalesmanLogin(BaseModel):
    salesman_name: str
    salesman_password: str
    
    class Config:
        form_attributes = True
    
class SalesmanEdit(BaseModel):
    salesman_name: str
    salesman_email: EmailStr
    salesman_contact : str
    salesman_password : str
    
    class Config:
        form_attributes = True
