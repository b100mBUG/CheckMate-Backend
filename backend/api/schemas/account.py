from pydantic import BaseModel
from pydantic import EmailStr

class AccountIn(BaseModel):
    company_id: int
    account_name: str
    account_email: str
    account_contact: str
    account_type: str
    account_password: str
    
    class Config:
        form_attributes = True

class AccountOut(BaseModel):
    account_id: int
    company_id: int
    account_name: str
    account_email: str
    account_contact: str
    account_type: str
    
    class Config:
        form_attributes = True

class AccountLogin(BaseModel):
    account_name: str
    account_password: str
    
    class Config: 
        form_attributes = True
    
class AccountEdit(BaseModel):
    account_name: str
    account_email: str
    account_contact: str
    account_type: str
    account_password: str
    
    class Config:
        form_attributes = True