from pydantic import BaseModel


class newItem(BaseModel):
    category : str
    item : str
    quantity : int
    unit : str

class updatePurchase(BaseModel):
    item : str
    quantity : int
    unit : str

class deleteCategory(BaseModel):
    category : str

class deleteItem(BaseModel):
    item : str
