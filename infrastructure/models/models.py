from pydantic import BaseModel


class newItem(BaseModel):
    category : str
    item : str
    quantity : int
    unit : str

class create_user_request(BaseModel):
    username: str

class request_bodyMetrics(BaseModel):
    user : str
    age : int
    height : int
    weight : int
    gender : str
    exercise_per_week : int

class response_bodyMetrics(BaseModel):
    user : str
    age : int
    height : int
    weight : int
    gender : str
    BMI : float
    BMR : float
    TDEE : float

class updatePurchase(BaseModel):
    item : str
    quantity : int
    unit : str

class deleteCategory(BaseModel):
    category : str

class deleteItem(BaseModel):
    item : str
