from fastapi import HTTPException, APIRouter
from starlette.status import HTTP_404_NOT_FOUND

from src.core import models
from src.core.database import GetDBDep
from src.schemas.store import Store, CreateStore, DbStore, PatchStore

router = APIRouter(prefix="/admin/stores", tags=["Stores"])

@router.post("", response_model=Store)
def create_store(store: CreateStore, db: GetDBDep):
    db_store = models.Store(**store.model_dump())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store


@router.get("", response_model=list[Store])
def list_stores(db: GetDBDep):
    store_list = db.query(models.Store).all()

    return store_list


@router.get("/{store_id}", response_model=Store)
def get_store(store_id: int, db: GetDBDep):
    db_store = db.get(models.Store, store_id)
    if db_store is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Store not found")
    return db_store


@router.put("/{store_id}", response_model=Store)
def update_store(store_id: int, store: CreateStore, db: GetDBDep):
    db_store = db.get(models.Store, store_id)
    if db_store is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Store not found")

    db_store.name = store.name
    db.store.owner_id = store.owner_id

    db.commit()
    return db_store


@router.patch("/{store_id}", response_model=Store)
def patch_store(store_id: int, store: PatchStore, db: GetDBDep):
    db_store = db.get(models.Store, store_id)
    if db_store is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Store not found")
    if store.name:
        db_store.name = store.name
    if store.owner_id:
        db_store.owner_id = store.owner_id

    db.commit()
    return db_store


@router.delete("/{store_id}")
def delete_store(store_id: int, db: GetDBDep):
    db_store = db.get(models.Store, store_id)
    if db_store is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Store not found")
    db.delete(db_store)
    db.commit()
    return {"message": "Store deleted"}