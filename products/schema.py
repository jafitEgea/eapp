from pydantic import BaseModel, constr

class CategoryBase(BaseModel):
    name: constr(min_length=2 , max_length=50)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryInDBBase(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class Category(CategoryInDBBase):
    pass

class CategoryInDB(CategoryInDBBase):
    pass

class ProductBase(BaseModel):
    name: str
    quantity: int
    description: str
    price: float
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductInDBBase(ProductBase):
    id: int
    category: Category

    class Config:
        orm_mode = True

class Product(ProductInDBBase):
    pass

class ProductInDB(ProductInDBBase):
    pass
