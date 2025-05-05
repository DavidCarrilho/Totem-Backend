from fastapi import APIRouter

router = APIRouter(prefix="/admin/products", tags=["Products"])

@router.get("")
def list_products():
    return []