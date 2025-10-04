from backend.database.actions.salesman import add_salesman, edit_salesman, delete_salesman, activate_salesman, show_salesmen, search_salesmen, deactivate_salesman, signin
from fastapi import APIRouter, HTTPException
from backend.api.schemas.salesman import SalesmanIn, SalesmanLogin, SalesmanOut, SalesmanEdit

router = APIRouter()

@router.get("/salesman-fetch/", response_model=list[SalesmanOut])
async def fetch_salesmen(sort_term: str, sort_dir: str):
    salesmen = await show_salesmen(sort_term, sort_dir)
    if not salesmen:
        raise HTTPException(status_code=404, detail="salesmen not found")
    return salesmen

@router.get("/salesman-search/", response_model=list[SalesmanOut])
async def find_salesmen(search_term: str):
    salesmen = await search_salesmen(search_term)
    if not salesmen:
        raise HTTPException(status_code=404, detail="salesmen not found")
    return salesmen

@router.post("/salesman-create/", response_model=SalesmanOut)
async def create_salesman(detail: SalesmanIn):
    try:
        new_salesman = await add_salesman(detail.model_dump())
        if not new_salesman:
            raise HTTPException(status_code=400, detail="failed to add salesman")
        return new_salesman
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.post("/salesman-login/", response_model=SalesmanOut)
async def login_account(detail: SalesmanLogin):
    salesman_detail = {
        'name': detail.salesman_name,
        'password': detail.salesman_password
    }
    try:
        salesman = await signin(salesman_detail)
        if not salesman:
            raise HTTPException(status_code=404, detail="salesman not found")
        return salesman
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.put("/salesman-activate/")
async def make_active(salesman_id: int):
    try:
        salesman = await activate_salesman(salesman_id)
        if not salesman:
            raise HTTPException(status_code=404, detail="salesman not found")
        return salesman
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.put("/salesman-deactivate/")
async def make_inactive(salesman_id: int):
    try:
        salesman = await deactivate_salesman(salesman_id)
        if not salesman:
            raise HTTPException(status_code=404, detail="salesman not found")
        return salesman
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.put("/salesman-edit/")
async def format_salesman(salesman_id: int, detail: SalesmanEdit):
    try:
        salesman = await edit_salesman(salesman_id, detail.model_dump())
        if not salesman:
            raise HTTPException(status_code=404, detail="salesman not found")
        return salesman
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.delete("/salesman-delete/")
async def remove_salesman(salesman_id: int):
    try:
        await delete_salesman(salesman_id)
        return {"message": "salesman deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")