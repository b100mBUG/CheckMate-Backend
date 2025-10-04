from backend.database.actions.company import add_company, edit_company, show_companies, search_companies, delete_company, signin
from fastapi import APIRouter, HTTPException
from backend.api.schemas.company import CompanyIn, CompanyOut, CompanyLogin

router = APIRouter()

@router.get("/companies-fetch/", response_model=list[CompanyOut])
async def fetch_companies(sort_dir: str, sort_term: str = "all"):
    companies = await show_companies(sort_term, sort_dir)
    if not companies:
        raise HTTPException(status_code=404, detail="Companies not found")
    return companies

@router.get("/companies-search/", response_model=list[CompanyOut])
async def find_companies(search_term: str):
    companies = await search_companies(search_term)
    if not companies:
        raise HTTPException(status_code=404, detail="Company not found")
    return companies

@router.post("/companies-create/", response_model = CompanyOut)
async def register_companies(company: CompanyIn):
    try:
        new_company = await add_company(company_detail=company.model_dump())
        return new_company
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.post("/companies-login/", response_model=CompanyOut)
async def login(credential: CompanyLogin):
    details = {
            "name": credential.company_name,
            "password": credential.company_password
        }
    try:
        company = await signin(company_detail=details)
        if not company:
            raise HTTPException(status_code=404, detail="company not found")
        return company
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
            

@router.put("/companies-edit/", response_model=CompanyOut)
async def format_company(company_id: int, detail: CompanyIn):
    try:
        company = await edit_company(company_id, detail.model_dump())
        if not company:
            raise HTTPException(status_code=404, detail="company not found")
        return company
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.delete("/companies-delete/")
async def remove_company(company_id: int):
    try:
        await delete_company(company_id)
        return {"message": "company deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")