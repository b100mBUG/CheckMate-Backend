from backend.database.actions.orders import (
    add_order, edit_order, delete_order, 
    search_orders, show_orders, clear_order, 
    get_salesman_specific_orders, search_salesman_orders
)
from fastapi import APIRouter, HTTPException
from backend.api.schemas.orders import OrderIn, OrderOut, OrderEdit

router = APIRouter()

@router.get("/orders-fetch/", response_model=list[OrderOut])
async def fetch_orders(filter_term: str, filter_dir: str):
    orders = await show_orders(filter_term, filter_dir)
    if not orders:
        raise HTTPException(status_code=404, detail="orders not found")
    return orders

@router.get("/orders-fetch-salesman/", response_model=list[OrderOut])
async def fetch_orders(salesman_id: int, filter_term: str, filter_dir: str):
    orders = await get_salesman_specific_orders(salesman_id, filter_term, filter_dir)
    if not orders:
        raise HTTPException(status_code=404, detail="orders not found")
    return orders

@router.get("/orders-search/", response_model=list[OrderOut])
async def find_orders(search_by: str, search_term: str):
    orders = await search_orders(search_by, search_term)
    if not orders:
        raise HTTPException(status_code=404, detail="orders not found")
    return orders

@router.get("/orders-salesman-search/", response_model=list[OrderOut])
async def find_orders(salesman_id: int, search_by: str, search_term: str):
    orders = await search_salesman_orders(salesman_id, search_by, search_term)
    if not orders:
        raise HTTPException(status_code=404, detail="orders not found")
    return orders

@router.post("/orders-create/", response_model=OrderOut)
async def create_order(detail: OrderIn):
    try:
        new_order = await add_order(detail.model_dump())
        return new_order
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.put("/order-edit/", response_model=OrderOut)
async def format_order(order_id: int, detail: OrderEdit):
    try: 
        order = await edit_order(order_id, detail.model_dump())
        if not order: 
            raise HTTPException(status_code=404, detail="order not found")
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.put("/order-clear/", response_model=OrderOut)
async def check_order(order_id: int):
    try:
        order = await clear_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="order not found")
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.delete("/order-delete/")
async def remove_order(order_id: int):
    try:
        await delete_order(order_id)
        return {"message": "order deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")