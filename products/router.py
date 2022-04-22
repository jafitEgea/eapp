from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import Any, List

from database import db
from . import schema
from . import services
from . import validation
from core import security
from users import schema as user_schema

api_router = APIRouter(tags = ["Products"])

@api_router.post("/products/category", status_code=status.HTTP_201_CREATED)
async def create_category(category_in: schema.CategoryCreate, db_session: Session = Depends(db.get_db_session)) -> Any:
    new_category = await services.create_new_category(category = category_in, db_session = db_session)
    return new_category

@api_router.get("/products/category", response_model = List[schema.Category])
async def get_all_categories(db_session: Session = Depends(db.get_db_session)):
    return await services.get_all_categories(db_session)

@api_router.get("/products/category/{category_id}", response_model = schema.Category)
async def get_category_by_id(category_id: int, db_session: Session = Depends(db.get_db_session)):
    category = await services.get_category_by_id(category_id, db_session)
    if not category:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Category not found")
    
    return category    

@api_router.delete("/products/category/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_by_id(category_id: int, db_session: Session = Depends(db.get_db_session)):
    category = await services.get_category_by_id(category_id, db_session)
    if not category:
        raise HTTPException(status_code=404, detail = "You have provided invalid category id")
    
    return await services.delete_category_by_id(category_id, db_session)

@api_router.put('/products/category/{category_id}', status_code = status.HTTP_201_CREATED)
async def update_category(category_id: int, category: schema.CategoryUpdate, db_session: Session = Depends(db.get_db_session)):
    new_category = await services.update_category(category_id, category, db_session)
    if not new_category:
        raise HTTPException(status_code=404, detail = "You have provided invalid category id")
    return new_category


@api_router.post("/products/", status_code = status.HTTP_201_CREATED)
async def create_product(product_in: schema.ProductCreate, db_session: Session = Depends(db.get_db_session),
                         current_user: user_schema.User = Depends(security.get_current_user)):
    category = await validation.verify_category_exist(product_in.category_id, db_session)
    if not category:
        raise HTTPException(status_code = 404, detail = "You have provided invalid category id.")

    new_product = await services.create_new_product(product = product_in, db_session = db_session)
    return new_product

@api_router.get("/products/", response_model = List[schema.Product])
async def get_all_products(db_session: Session = Depends(db.get_db_session)):
    return await services.get_all_products(db_session)

@api_router.get("/products/{product_id}", response_model = schema.Product)
async def get_product_by_id(product_id: int, db_session: Session = Depends(db.get_db_session)):
    product = await services.get_product_by_id(product_id, db_session)
    if not product:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Product not found")
    
    return product    

@api_router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_by_id(product_id: int, db_session: Session = Depends(db.get_db_session)):
    product = await services.get_product_by_id(product_id, db_session)
    if not product:
        raise HTTPException(status_code=404, detail = "You have provided invalid product id")
    
    return await services.delete_product_by_id(product_id, db_session)

@api_router.put('/products/{product_id}', status_code = status.HTTP_201_CREATED)
async def update_product(product_id: int, product: schema.ProductUpdate, db_session: Session = Depends(db.get_db_session)):
    new_product = await services.update_product(product_id, product, db_session)
    if not new_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return new_product