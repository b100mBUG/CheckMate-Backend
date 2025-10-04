from pydantic import BaseModel
from pydantic import EmailStr

class CompanyIn(BaseModel):
    company_name: str
    company_email: EmailStr
    company_contact: str
    company_password: str
    
    class Config:
        form_attributes = True

class CompanyOut(BaseModel):
    company_id: int
    company_name: str
    company_email: EmailStr
    company_contact: str
    
    class Config:
        form_attributes = True

class CompanyLogin(BaseModel):
    company_name: str
    company_password: str
    
    class Config:
        form_attributes = True